from json import dump
from time import sleep
import krpc


def get_statistics():
    conn = krpc.connect(name='Vostok-6')
    vessel = conn.space_center.active_vessel

    data = []
    start_time = conn.space_center.ut
    stage = 0
    last_mass = vessel.dry_mass
    srf_frame = vessel.orbit.body.reference_frame

    vessel.control.throttle = 1.0
    vessel.control.sas = True
    vessel.control.activate_next_stage()

    while conn:
        time_from_launch = conn.space_center.ut - start_time

        if stage == 3:
            conn = False

        if last_mass - vessel.dry_mass > 10:
            last_mass = vessel.dry_mass
            stage += 1

        data.append([time_from_launch, vessel.flight(srf_frame).speed])
        print(stage, vessel.flight(srf_frame).speed, time_from_launch)
        sleep(0.25)

    with open('flight_data.json', 'w') as f:
        dump(data, f)
