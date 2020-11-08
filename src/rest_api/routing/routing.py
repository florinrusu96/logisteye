import json
from math import sin, cos, sqrt, atan2, radians, asin
from rest_api.models import Locker, Package, Box, User, Area, CourierToPackage, Location
from rest_api.serializers import AreaSerializer, PackageSerializer, LockerSerializer
from simulation.generators.utils import *
from rest_api import models
from django.db.models import Count
import random

DEFAULT_COURIER_RADIUS = 3


routed_to = {}


def run_routing_algorithm():
    for courier in User.objects.all():
        courier.assigned_area = None
        courier.save()

    global routed_to
    routed_to = {}

    packages = retrieve_packages()
    lockers = retrieve_lockers()

    distribute_on_the_margins(packages, lockers)

    work_to_do = True
    cut_off = 10
    while work_to_do and cut_off > 0:
        work_to_do = assign_couriers(packages)
        cut_off -= 1

    distribute_worker_among_couriers()


def distribute_worker_among_couriers():
    work_free_couriers = [bike for bike in models.User.objects.filter(assigned_area__isnull=True)]
    while len(work_free_couriers) != 0:
        over_worked_courier = models.User.objects \
            .annotate(num_courierToPackage=Count('couriertopackage')) \
            .order_by('num_courierToPackage') \
            .filter(assigned_area__isnull=False) \
            .first()

        courier_to_pack_duty = [courier_to_pack for courier_to_pack in
                                CourierToPackage.objects.filter(courier=over_worked_courier)]
        if len(courier_to_pack_duty) < 5:
            break

        lucky_fellow = work_free_couriers[0]
        lucky_fellow.assigned_area = over_worked_courier.assigned_area
        lucky_fellow.save()
        for courier_to_pack in courier_to_pack_duty[::2]:
            courier_to_pack.courier = lucky_fellow
            courier_to_pack.save()


def assign_couriers(packages):
    not_delivered_packages = [package for package in packages if not package.is_delivered]
    if len(not_delivered_packages) == 0:
        return False
    print(f"Not delivered: {len(not_delivered_packages)}")
    unused_bikes = models.User.objects.filter(assigned_area__isnull=True).count()
    print(f"Unused bikes: {unused_bikes}")

    for package in not_delivered_packages:
        assign_best_courier_for_package(package)
    return True


def shift_area_to_include_location(area, location):
    dist = compute_distance(area.location_center, location)
    distance_to_area = dist - area.radius
    if distance_to_area < 0:
        return area

    angle = compute_angle_for_coordinates(area.location_center, location)
    p = apply_distance_to_location_in_direction(area.location_center.latitude,
                                                area.location_center.longitude,
                                                distance_to_area, angle)
    shifted_area_center = Location(latitude=p[0], longitude=p[1])
    return Area(location_center=shifted_area_center, radius=area.radius)


def check_courier_can_cover_package(courier, package):
    global routed_to
    if check_area_contains(courier.assigned_area, routed_to[package]):
        return True

    dist = compute_distance(courier.assigned_area.location_center, routed_to[package])
    current_dist_of_packet = compute_distance(routed_to[package], package.destination_location)

    # If packet is already close than my courier, it doesn't make sense to use this courier
    if dist > current_dist_of_packet:
        return False

    shifted_area = shift_area_to_include_location(courier.assigned_area, routed_to[package])
    previous_assignments = CourierToPackage.objects.filter(courier=courier).all()
    for assignment in previous_assignments:
        if not check_area_contains(shifted_area, assignment.pickup_location):
            return False

    return True


def find_best_locker_in_courier_area(package, courier):
    lockers_in_area = [locker for locker in Locker.objects.all()
                       if check_area_contains(courier.assigned_area, locker.location)]
    if len(lockers_in_area) == 0:
        # debug_all_data()
        return None

    distances = [compute_distance(locker.location, package.destination_location) for locker in lockers_in_area]
    index_min = min(range(len(distances)), key=distances.__getitem__)
    return lockers_in_area[index_min]


def debug_all_data():
    lockers = [locker for locker in Locker.objects.all()]
    bike_areas = [user.assigned_area for user in User.objects.filter(assigned_area__isnull=False)]
    packages = [package for package in Package.objects.all()]

    print(json.dumps([LockerSerializer(instance=locker).data for locker in lockers]))
    print(json.dumps([AreaSerializer(instance=area).data for area in bike_areas]))
    print(json.dumps([PackageSerializer(instance=package).data for package in packages]))


def assign_best_courier_for_package(package):
    global routed_to
    couriers = User.objects.all()

    for courier in couriers:
        if courier.assigned_area is None:
            continue

        if check_area_contains(courier.assigned_area, routed_to[package]) \
                and check_area_contains(courier.assigned_area, package.destination_location):
            package.is_delivered = True
            package.save()
            return

        if not check_courier_can_cover_package(courier, package):
            continue

        assigned_area = shift_area_to_include_location(courier.assigned_area, routed_to[package])
        courier.assigned_area = assigned_area

        drop_off_locker = find_best_locker_in_courier_area(package, courier)
        if drop_off_locker is None or drop_off_locker.location == routed_to[package]:
            continue

        assigned_area.location_center.save()
        assigned_area.save()
        courier.save()
        assign_courier_for_package(courier, package, drop_off_locker)
        return

    for courier in couriers:
        if courier.assigned_area is not None:
            continue

        assigned_area_center = compute_point_in_disk(routed_to[package], package.destination_location,
                                                     2 / 3 * DEFAULT_COURIER_RADIUS)
        assigned_area = Area(location_center=assigned_area_center, radius=DEFAULT_COURIER_RADIUS)

        courier.assigned_area = assigned_area
        drop_off_locker = find_best_locker_in_courier_area(package, courier)
        if drop_off_locker is None:
            courier.assigned_area = None
            continue

        assigned_area_center.save()
        assigned_area.save()
        courier.save()
        assign_courier_for_package(courier, package, drop_off_locker)
        return


def assign_courier_for_package(courier, package, drop_off_locker):
    global routed_to
    CourierToPackage.objects.create(**{
        "package": package,
        "courier": courier,
        "pickup_location": package.current_box.locker.location,
        "drop_off_location": drop_off_locker.location
    })
    routed_to[package] = drop_off_locker.location


def retrieve_lockers():
    return Locker.objects.all()


def retrieve_packages():
    return Package.objects.all()


def assign_package_to_starting_locker(package, starting_locker):
    global routed_to
    boxes = Box.objects.filter(locker=starting_locker).filter(is_empty=True)
    assigned_box = boxes.first()
    package.source_location = starting_locker.location
    package.current_location = starting_locker.location
    package.current_box = assigned_box
    package.save()

    assigned_box.is_empty = False
    assigned_box.save()
    routed_to[package] = starting_locker.location


def check_locker_has_empty_boxes(locker):
    return Box.objects.filter(locker_id=locker.id, is_empty=True).count() != 0


def distribute_on_the_margins(packages, lockers):
    remote_lockers = identify_margins(lockers)
    print(f"Remote lockers: {len(remote_lockers)}")
    packages_to_distribute = [p for p in packages]

    while len(packages_to_distribute) != 0 and len(remote_lockers) != 0:
        package = packages_to_distribute[0]
        if len(remote_lockers) == 0:
            return

        distance_to_lockers = [compute_distance(package.destination_location, locker.location)
                               for locker in remote_lockers]

        index_min = min(range(len(distance_to_lockers)), key=distance_to_lockers.__getitem__)
        best_locker = remote_lockers[index_min]
        if not check_locker_has_empty_boxes(best_locker):
            remote_lockers.remove(best_locker)
        else:
            assign_package_to_starting_locker(package, best_locker)
            packages_to_distribute.remove(package)


def get_distance_to_center(locker):
    return compute_distance(locker.location, get_center_area().location_center)


def get_center_area():
    result = models.area.Area()
    result.location_center = Location(latitude=PARIS_CENTER_LAT, longitude=PARIS_CENTER_LONG)

    result.radius = 5

    return result


def compute_distance(point_1, point_2):
    lat1 = radians(point_1.latitude)
    lon1 = radians(point_1.longitude)
    lat2 = radians(point_2.latitude)
    lon2 = radians(point_2.longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R_EARTH * c


def compute_angle_for_coordinates(point_1, point_2):
    aux_point = Location(latitude=point_1.latitude, longitude=point_2.longitude)
    dlat = compute_distance(point_1, aux_point)
    dist = compute_distance(point_1, point_2)

    return asin(dlat / dist)


def compute_point_in_disk(point_1, point_2, radius):
    angle = compute_angle_for_coordinates(point_1, point_2)
    p = apply_distance_to_location_in_direction(point_1.latitude, point_1.longitude, radius, angle)
    return Location(latitude=min(p[0], point_2.latitude), longitude=min(p[1], point_2.longitude))


def check_area_contains(area, location):
    return compute_distance(area.location_center, location) < area.radius


def identify_margins(lockers):
    return [locker for locker in lockers if not check_area_contains(get_center_area(), locker.location)]


def apply_distance_to_location_in_direction(lat, long, dist, angle):
    return apply_distance_to_location(lat, long, dist * cos(angle), dist * sin(angle))


def compute_time_needed_for_deliveries():
    couriers = [courier for courier in models.User.objects.filter(assigned_area__isnull=False)]
    packages = [package for package in models.Package.objects.all()]
    courier_to_package = [courier_to_package for courier_to_package in models.CourierToPackage.objects.all()]
    resolver = TimeResolver(couriers, packages, courier_to_package)

    return resolver.resolve() * 20


def compute_saved_co2():
    time = compute_time_needed_for_deliveries()
    return random.uniform(0.491, 0.522) * time / 60


class CourierState:
    def __init__(self, location):
        self.location = location
        self.transport = None


class TimeResolver:
    def __init__(self, couriers, packages, courier_to_package):
        self.current_time = 0
        self.courier_states = {}
        self.package_locations = {}

        self.couriers = couriers
        self.packages = packages
        self.courier_to_package = courier_to_package
        self.fulfilled_transports = []

    def step(self):
        active_couriers = [courier for courier in self.couriers
                           if self.courier_states[courier].transport is not None]
        for courier in active_couriers:
            transport = self.courier_states[courier].transport
            package = transport.package

            self.fulfilled_transports.append(transport)
            self.package_locations[package] = transport.drop_off_location
            self.courier_states[courier].transport = None

        active_transports = [transport for transport in self.courier_to_package
                             if transport.pickup_location == self.package_locations[transport.package]]
        for transport in active_transports:
            if self.courier_states[transport.courier].transport is not None:
                continue

            self.courier_states[transport.courier].transport = transport

        self.current_time += 1

    def resolve(self):
        for package in self.packages:
            self.package_locations[package] = package.source_location

        for courier in self.couriers:
            self.courier_states[courier] = CourierState(courier.assigned_area.location_center)

        while len(self.fulfilled_transports) < len(self.courier_to_package):
            print(f"Fulfilled: {len(self.fulfilled_transports)}; Total: {len(self.courier_to_package)} ")
            self.step()

        return self.current_time
