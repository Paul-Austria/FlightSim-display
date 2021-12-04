from SimConnect import *
import logging
from SimConnect.Enum import *
from time import sleep
import serial
import math
import json

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.info("START")
# time holder for inline commands
ct_g = millis()

# creat simconnection and pass used user classes
sm = SimConnect()
aq = AircraftRequests(sm, _time=200)
ae = AircraftEvents(sm)

def trigger_event(event_name, value_to_use = None):
	# This function actually does the work of triggering the event

	EVENT_TO_TRIGGER = ae.find(event_name)
	if EVENT_TO_TRIGGER is not None:
		if value_to_use is None:
			EVENT_TO_TRIGGER()
		else:
			EVENT_TO_TRIGGER(int(value_to_use))

		status = "success"
	else:
		status = "Error: %s is not an Event" % (event_name)

	return status

def set_datapoint(datapoint_name, index=None, value_to_use=None):
	# This function actually does the work of setting the datapoint

	if index is not None and ':index' in datapoint_name:
		clas = aq.find(datapoint_name)
		if clas is not None:
			clas.setIndex(int(index))

	sent = False
	if value_to_use is None:
		sent = aq.set(datapoint_name, 0)
	else:
		sent = aq.set(datapoint_name, int(value_to_use))

	if sent is True:
		status = "success"
	else:
		status = "Error with sending request: %s" % (datapoint_name)

	return status


# THROTTLE1 Request
Throttle = aq.find('GENERAL_ENG_THROTTLE_LEVER_POSITION:1')
while not sm.quit:
	#print(set_datapoint('GEAR_HANDLE_POSITION', None, 1)); # extend gear


	data = {};
	data['ALT'] = aq.PositionandSpeedData.get('PLANE_ALTITUDE');
	data['LAT'] = aq.PositionandSpeedData.get('PLANE_LATITUDE');
	data['LNG'] = aq.PositionandSpeedData.get('PLANE_LONGITUDE');
	data['SPD'] = aq.FlightInstrumentationData.get('AIRSPEED_INDICATED');
	data['GRH'] = aq.LandingGearData.get('GEAR_HANDLE_POSITION');
	data['GEP'] = aq.LandingGearData.get('GEAR_CENTER_POSITION');
	data['TRM'] = aq.ControlsData.get('ELEVATOR_TRIM_PCT')
	data['FLP'] = aq.ControlsData.get('FLAPS_HANDLE_PERCENT');
	data['VSPD'] = aq.FlightInstrumentationData.get('VERTICAL_SPEED');
	data['DEG'] = math.degrees(aq.FlightInstrumentationData.get('HEADING_INDICATOR'));
	data['OWR'] = aq.FlightInstrumentationData.get('OVERSPEED_WARNING');
	data['SWR'] = aq.FlightInstrumentationData.get('STALL_WARNING');
	data['FUL'] = aq.FuelData.get('FUEL_SELECTED_QUANTITY_PERCENT');
	data['THR'] = Throttle.value;
	print(json.dumps(data));
	sleep(0.2)

sm.exit()
