import os
import json
import dirigera
import openai
from dotenv import load_dotenv
from GetJsonData import *

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

dirigera_hub = dirigera.Hub(
    token=os.getenv('DIRIGERA_TOKEN'),
    ip_address=os.getenv('DIRIGERA_IP'),
    # port=os.getenv('DIRIGERA_PORT')
)

BUFFER_FILE = "buffer.json"
MAX_PROMPTS = 50

def load_buffer():
    if os.path.exists(BUFFER_FILE):
        with open(BUFFER_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_buffer(buffer):
    with open(BUFFER_FILE, 'w') as f:
        json.dump(buffer, f)

def add_prompt_to_buffer(prompt, output):
    buffer = load_buffer()
    buffer[prompt] = output
    if len(buffer) > MAX_PROMPTS:
        oldest_prompt = next(iter(buffer))
        del buffer[oldest_prompt]
    save_buffer(buffer)

def get_output_from_buffer(prompt):
    buffer = load_buffer()
    return buffer.get(prompt)

def format_prompt_output(prompt, output):
    return f'"{prompt}": "{output}"'

def process_prompt(prompt):
    output = get_output_from_buffer(prompt)
    if output is None:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": "system",
                    "content": "Respond with ONLY a Python program WITHOUT COMMENTS(#comment), And do not make it a/in code block. The IKEA smart home docs is:\n\nControlling Lights\n\nTo get information about the available lights, you can use the `get_lights()` method:\n\nlights = dirigera_hub.get_lights()\n\nThe light object has the following attributes:\n\n- device_id: str\n- is_reachable: bool\n- custom_name: str\n- is_on: bool\n- startup_on_off: StartupEnum | None\n- light_level: int | None  # Not all lights have a light level\n- color_temp: int | None  # Not all lights have a color temperature\n- color_temp_min: int | None\n- color_temp_max: int | None\n- color_hue: int | None  # Not all lights have a color hue\n- color_saturation: float | None  # Not all lights have a color saturation\n- room_id: str\n- room_name: str\n- can_receive: List[str]  # list of all available commands [\"customName\", \"isOn\", \"lightLevel\", ...]\n\nAvailable methods for light are:\n\n- light.set_name(name=\"kitchen light 1\")\n- light.set_light(lamp_on=True)\n- light.set_light_level(light_level=90)\n- light.set_color_temperature(color_temp=3000)\n- light.set_light_color(hue=128, saturation=0.5)\n- light.set_startup_behaviour(behaviour=StartupEnum.START_OFF)\n\nAn additional method for light is:\n\n- dirigera_hub.get_light_by_name(name=\"kitchen light 1\")\n\nControlling Outlets\n\nTo get information about the available outlets, you can use the `get_outlets()` method:\n\noutlets = dirigera_hub.get_outlets()\n\nThe outlet object has the following attributes:\n\n- device_id: str\n- is_reachable: bool\n- custom_name: str\n- is_on: bool\n- startup_on_off: StartupEnum | None\n- room_id: str\n- room_name: str\n- can_receive: List[str]  # list of all available commands [\"customName\", \"isOn\", \"lightLevel\", ...]\n\nAvailable methods for outlet are:\n\n- outlet.set_name(name=\"kitchen socket 1\")\n- outlet.set_on(outlet_on=True)\n- outlet.set_startup_behaviour(behaviour=StartupEnum.START_OFF)\n\nControlling Blinds\n\nTo get information about the available blinds, you can use the `get_blinds()` method:\n\nblinds = dirigera_hub.get_blinds()\n\nThe blind object has the following attributes:\n\n- device_id: str\n- is_reachable: bool\n- custom_name: str\n- target_level: int\n- current_level: int\n- state: str\n- room_id: str\n- room_name: str\n- can_receive: List[str]  # list of all available commands [\"customName\", \"blindsCurrentLevel\", \"blindsTargetLevel\", \"blindsState\"]\n\nAvailable methods for blinds are:\n\n- blind.set_name(name=\"kitchen blind 1\")\n- blind.set_target_level(target_level=90) target_level=100 means that the blinds roll all the way down\n\nRemote Controllers\n\nCurrently only tested with the STYRBAR remote.\n\nTo get information about the available controllers, you can use the `get_controllers()` method:\n\ncontrollers = dirigera_hub.get_controllers()\n\nThe controller object has the following attributes:\n\n- device_id: str\n- is_reachable: bool\n- custom_name: str\n- is_on: bool\n- battery_percentage: int\n- room_id: str\n- room_name: str\n- can_receive: List[str]  # list of all available commands [\"customName\"]\n\nAvailable methods for the controller are:\n\n- controller.set_name(name=\"kitchen remote 1\")\n\nEnvironment Sensor\n\nCurrently only tested with the VINDSTYRKA sensor. If you have other sensors, please send me the JSON, and I will add support or create a PR.\n\nTo get the environment sensors, use:\n\nsensors = dirigera_hub.get_environment_sensors()\n\nThe environment sensor object has the following attributes:\n\n- device_id: str\n- is_reachable: bool\n- custom_name: str\n- current_temperature: str\n- current_rh: int  # current humidity\n- current_pm25: int  # current particulate matter 2.5\n- max_measured_pm25: int  # maximum measurable particulate matter 2.5\n- min_measured_pm25: int  # minimum measurable particulate matter 2.5\n- voc_index: int  # current volatile organic compound\n- room_id: str\n- room_name: str\n- can_receive: list[str]  # list of all available commands [\"customName\"]\n\nEvent Listener\n\nThe event listener allows you to listen to events that are published by your Dirigera hub. This is useful if you want to automate tasks based on events such as when a light is turned on or off or when the color temperature of a light is changed.\n\nimport json\nfrom typing import Any\n\ndef on_message(ws: Any, message: str):\n    message_dict = json.loads(message)\n    data = message_dict[\"data\"]\n    if data[\"id\"] == bed_light.light_id:\n        print(f\"{message_dict['type']} event on {bed_light.custom_name}, attributes: {data['attributes']}\")\n\ndef on_error(ws: Any, message: str):\n    print(message)\n\ndirigera_hub.create_event_listener(\n    on_message=on_message, on_error=on_error\n)\n\ndeviceStateChanged event on Bed Light, attributes: {'isOn': False}\n\nAnd this is my device:\n{data}"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        output = response["choices"][0]["message"]["content"]
        add_prompt_to_buffer(prompt, output)
    
    return format_prompt_output(prompt, output)

prompt = "hi"
output = process_prompt(prompt)
print(output)
