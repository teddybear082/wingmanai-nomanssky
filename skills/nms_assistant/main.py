import requests
import json
from typing import TYPE_CHECKING
from api.enums import LogType
from api.interface import (
    SettingsConfig,
    SkillConfig,
    WingmanConfig,
    WingmanInitializationError,
)
from skills.skill_base import Skill
import asyncio

if TYPE_CHECKING:
    from wingmen.wingman import Wingman

API_BASE_URL = "https://api.nmsassistant.com"

class NMSAssistant(Skill):
    def __init__(
        self,
        config: SkillConfig,
        wingman_config: WingmanConfig,
        settings: SettingsConfig,
        wingman: "Wingman",
    ) -> None:
        super().__init__(config=config, wingman_config=wingman_config, settings=settings, wingman=wingman)

    async def validate(self) -> list[WingmanInitializationError]:
        errors = await super().validate()
        return errors

    def get_tools(self) -> list[tuple[str, dict]]:
        tools = [
            (
                "get_release_info",
                {
                    "type": "function",
                    "function": {
                        "name": "get_release_info",
                        "description": "Fetch release information from No Man's Sky website.",
                    },
                },
            ),
            (
                "get_news",
                {
                    "type": "function",
                    "function": {
                        "name": "get_news",
                        "description": "Fetch news from No Man's Sky website.",
                    },
                },
            ),
            (
                "get_community_mission_info",
                {
                    "type": "function",
                    "function": {
                        "name": "get_community_mission_info",
                        "description": "Fetch current community mission information.",
                    },
                },
            ),
            (
                "get_latest_expedition_info",
                {
                    "type": "function",
                    "function": {
                        "name": "get_latest_expedition_info",
                        "description": "Fetch latest expedition information.",
                    },
                },
            ),
            (
                "get_item_info_by_name",
                {
                    "type": "function",
                    "function": {
                        "name": "get_item_info_by_name",
                        "description": "Fetch game item details based on name and language.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "The name of the item.",
                                },
                                "languageCode": {
                                    "type": "string",
                                    "description": "The language code (e.g., 'en' for English)",
                                },
                            },
                            "required": ["name", "languageCode"],
                        },
                    },
                },
            ),
            (
                "get_extra_item_info",
                {
                    "type": "function",
                    "function": {
                        "name": "get_extra_item_info",
                        "description": "Fetch extra item details using AppId.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "appId": {
                                    "type": "string",
                                    "description": "The AppId of the item.",
                                },
                                "languageCode": {
                                    "type": "string",
                                    "description": "The language code (e.g., 'en' for English)",
                                },
                            },
                            "required": ["appId", "languageCode"],
                        },
                    },
                },
            ),
            (
                "get_refiner_recipes_by_input",
                {
                    "type": "function",
                    "function": {
                        "name": "get_refiner_recipes_by_input",
                        "description": "Fetch refiner recipes by input item using AppId.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "appId": {
                                    "type": "string",
                                    "description": "The AppId of the item.",
                                },
                                "languageCode": {
                                    "type": "string",
                                    "description": "The language code (e.g., 'en' for English)",
                                },
                            },
                            "required": ["appId", "languageCode"],
                        },
                    },
                },
            ),
            (
                "get_refiner_recipes_by_output",
                {
                    "type": "function",
                    "function": {
                        "name": "get_refiner_recipes_by_output",
                        "description": "Fetch refiner recipes by output item using AppId.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "appId": {
                                    "type": "string",
                                    "description": "The AppId of the item.",
                                },
                                "languageCode": {
                                    "type": "string",
                                    "description": "The language code (e.g., 'en' for English)",
                                },
                            },
                            "required": ["appId", "languageCode"],
                        },
                    },
                },
            ),
            (
                "get_cooking_recipes_by_input",
                {
                    "type": "function",
                    "function": {
                        "name": "get_cooking_recipes_by_input",
                        "description": "Fetch cooking recipes by input item using AppId.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "appId": {
                                    "type": "string",
                                    "description": "The AppId of the item.",
                                },
                                "languageCode": {
                                    "type": "string",
                                    "description": "The language code (e.g., 'en' for English)",
                                },
                            },
                            "required": ["appId", "languageCode"],
                        },
                    },
                },
            ),
            (
                "get_cooking_recipes_by_output",
                {
                    "type": "function",
                    "function": {
                        "name": "get_cooking_recipes_by_output",
                        "description": "Fetch cooking recipes by output item using AppId.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "appId": {
                                    "type": "string",
                                    "description": "The AppId of the item.",
                                },
                                "languageCode": {
                                    "type": "string",
                                    "description": "The language code (e.g., 'en' for English)",
                                },
                            },
                            "required": ["appId", "languageCode"],
                        },
                    },
                },
            ),
        ]
        return tools

    async def request_api(self, endpoint: str) -> dict:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    async def parse_nms_assistant_api_response(self, api_response) -> dict:
        def extract_app_ids(data):
            app_ids = []
            # Parse the JSON string into Python objects
            #data = json.loads(json_data)
            for entry in data:
                # Extract the appId from the main entry
                app_ids.append(entry['appId'])
                # Extract the appIds from the inputs
                for input_item in entry['inputs']:
                    app_ids.append(input_item['appId'])
                # Extract the appId from the output
                app_ids.append(entry['output']['appId'])
            return app_ids
        # Extract appIds
        app_ids = extract_app_ids(api_response)
        async def fetch_item_name(app_id: str) -> str:
            data = await self.request_api(f"/ItemInfo/{app_id}/en")
            return data.get('name', 'Unknown')
        # Get names for each appID as a key for the LLM
        tasks = [fetch_item_name(item) for item in app_ids]
        results = await asyncio.gather(*tasks)
        return {item: name for item, name in zip(app_ids, results)}

    async def execute_tool(self, tool_name: str, parameters: dict[str, any]) -> tuple[str, str]:
        function_response = "Operation failed."
        instant_response = ""

        if tool_name == "get_release_info":
            data = await self.request_api("/HelloGames/Release")
            function_response = data if data else function_response

        elif tool_name == "get_news":
            data = await self.request_api("/HelloGames/News")
            function_response = data if data else function_response

        elif tool_name == "get_community_mission_info":
            data = await self.request_api("/HelloGames/CommunityMission")
            function_response = data if data else function_response

        elif tool_name == "get_latest_expedition_info":
            data = await self.request_api("/HelloGames/Expedition")
            function_response = data if data else function_response

        elif tool_name == "get_item_info_by_name":
            name = parameters.get("name")
            language_code = parameters.get("languageCode")
            data = await self.request_api(f"/ItemInfo/Name/{name}/{language_code}")
            function_response = data if data else function_response

        elif tool_name == "get_extra_item_info":
            app_id = parameters.get("appId")
            language_code = parameters.get("languageCode")
            data = await self.request_api(f"/ItemInfo/ExtraProperties/{app_id}/{language_code}")
            function_response = data if data else function_response

        elif tool_name == "get_refiner_recipes_by_input":
            app_id = parameters.get("appId")
            language_code = parameters.get("languageCode")
            data = await self.request_api(f"/ItemInfo/RefinerByInput/{app_id}/{language_code}")
            if data:
                parsed_data = await self.parse_nms_assistant_api_response(data)
                function_response = f"{data}; key for item names used in above data: {parsed_data}"

        elif tool_name == "get_refiner_recipes_by_output":
            app_id = parameters.get("appId")
            language_code = parameters.get("languageCode")
            data = await self.request_api(f"/ItemInfo/RefinerByOutut/{app_id}/{language_code}")
            if data:
                parsed_data = await self.parse_nms_assistant_api_response(data)
                function_response = f"{data}; key for item names used in above data: {parsed_data}"

        elif tool_name == "get_cooking_recipes_by_input":
            app_id = parameters.get("appId")
            language_code = parameters.get("languageCode")
            data = await self.request_api(f"/ItemInfo/CookingByInput/{app_id}/{language_code}")
            if data:
                parsed_data = await self.parse_nms_assistant_api_response(data)
                function_response = f"{data}; key for item names used in above data: {parsed_data}"

        elif tool_name == "get_cooking_recipes_by_output":
            app_id = parameters.get("appId")
            language_code = parameters.get("languageCode")
            data = await self.request_api(f"/ItemInfo/CookingByOutut/{app_id}/{language_code}")
            if data:
                parsed_data = await self.parse_nms_assistant_api_response(data)
                function_response = f"{data}; key for item names used in above data: {parsed_data}"

        if self.settings.debug_mode:
            await self.printr.print_async(f"Executed {tool_name} with parameters {parameters}. Result: {function_response}", color=LogType.INFO)

        return function_response, instant_response