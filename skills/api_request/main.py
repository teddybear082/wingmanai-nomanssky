import json
import time
import random
import asyncio
from typing import Any, Dict, Tuple
import aiohttp
from aiohttp import ClientError
from api.enums import LogType
from api.interface import SettingsConfig, SkillConfig, WingmanConfig, WingmanInitializationError
from skills.skill_base import Skill

DEFAULT_HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Content-Security-Policy": "default-src 'self'",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Access-Control-Allow-Origin": "http://localhost",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Headers": "*",
}

class APIRequest(Skill):
    """Skill for making API requests."""

    def __init__(
        self,
        config: SkillConfig,
        wingman_config: WingmanConfig,
        settings: SettingsConfig,
        wingman: "Wingman",
    ) -> None:
        self.use_default_headers = False
        self.default_headers = DEFAULT_HEADERS
        self.max_retries = 1
        self.request_timeout = 5
        self.retry_delay = 5
        super().__init__(config=config, wingman_config=wingman_config, settings=settings, wingman=wingman)

    async def validate(self) -> list[WingmanInitializationError]:
        errors = await super().validate()

        self.use_default_headers = self.retrieve_custom_property_value(
            "use_default_headers", errors
        )

        self.max_retries = self.retrieve_custom_property_value(
            "max_retries", errors
        )
        self.request_timeout = self.retrieve_custom_property_value(
            "request_timeout", errors
        )
        self.retry_delay = self.retrieve_custom_property_value(
            "retry_delay", errors
        )
        return errors


    # Prepare and send API request using parameters provided by LLM response to function call
    async def _send_api_request(self, parameters: Dict[str, Any]) -> str:
        """Send an API request with the specified parameters."""
        # Get headers from LLM, check whether they are a dictionary, if not at least let user know in debug mode.
        headers = parameters.get("headers")
        if headers and isinstance(headers, dict):
            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Validated that headers returned from LLM is a dictionary.",
                    color=LogType.INFO,
                )
        elif headers:
            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Headers returned from LLM is not a dictionary.  Type is {type(headers)}",
                    color=LogType.INFO,
                )
        else:
            headers = {}

        # If using default headers, add those to AI generated headers
        if self.use_default_headers:
            headers.update(self.default_headers) # Defaults will override AI-generated if necessary
            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Default headers being used for API call: {headers}",
                    color=LogType.INFO,
                )

        # Get params, check whether they are a dictionary, if not, at least let user know in debug mode.
        params = parameters.get("params")
        if params and isinstance(params, dict):
            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Validated that params returned from LLM is a dictionary.",
                    color=LogType.INFO,
                )
        elif params:
            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Params returned from LLM is not a dictionary.  Type is {type(params)}",
                    color=LogType.INFO,
                )
        else:
            params = {}

        # Get body of request.  First check to see if LLM returned a "data" field, and if so, whether data is a dictionary, if not, at least let the user know in debug mode.
        body = parameters.get("data")
        if body and isinstance(body, dict):
            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Validated that data returned from LLM is a dictionary.",
                    color=LogType.INFO,
                )
        elif body:
            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Data returned from LLM is not a dictionary.  Type is {type(body)}",
                    color=LogType.INFO,
                )
        # 'data' was not present in parameters, so check if 'body' was provided instead.  If so, check whether body is a dictionary, and if not, at least let the user know in debug mode.
        else:
            body = parameters.get("body")
            if body and isinstance(body, dict):
                if self.settings.debug_mode:
                    await self.printr.print_async(
                        f"Validated that body returned from LLM is a dictionary.",
                        color=LogType.INFO,
                    )
            elif body:
                if self.settings.debug_mode:
                    await self.printr.print_async(
                        f"Body returned from LLM is not a dictionary.  Type is {type(body)}",
                        color=LogType.INFO,
                    )
            else:
                body = {} # Should this be None instead?

        # However we got the body for the request, try turning it into the valid json that aiohttp session.request expects for data field
        try:
            data = json.dumps(body)
        except:

            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Cannot convert data into valid json: {data}.",
                )
            data = json.dumps({}) # Just send an empty dictionary if everything else failed
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=parameters["method"],
                    url=parameters["url"],
                    headers=headers,
                    params=params,
                    data=data,
                    timeout=self.request_timeout
                ) as response:
                    response.raise_for_status()
                    return await response.text()
        except ClientError as request_exception:
            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Error with api request: {request_exception}.",
                    color=LogType.INFO,
                )
            return f"Error, could not complete API request. Exception was: {request_exception}."

        except asyncio.TimeoutError:
            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Error with api request: ayncio timeout.",
                    color=LogType.INFO,
                )
            return "Error, could not complete API request.  Timed out."

        except Exception as e:
            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Error with api request: {e}.",
                    color=LogType.INFO,
                )
            return f"Error, could not complete API request.  Reason was {e}."

    def get_tools(self) -> list[Tuple[str, Dict[str, Any]]]:
        return [
            (
                "send_api_request",
                {
                    "type": "function",
                    "function": {
                        "name": "send_api_request",
                        "description": "Send an API request with the specified method, headers, parameters, and body. Return the response back.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string", "description": "The URL for the API request."},
                                "method": {"type": "string", "description": "The HTTP method (GET, POST, PUT, PATCH, DELETE, etc.)."},
                                "headers": {"type": "object", "description": "Headers for the API request."},
                                "params": {"type": "object", "description": "URL parameters for the API request."},
                                "data": {"type": "object", "description": "Body or payload for the API request."},
                            },
                            "required": ["url", "method"],
                        },
                    },
                },
            ),
        ]

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Tuple[str, str]:
        function_response = "Error with API request, could not complete."
        instant_response = ""
        if tool_name == "send_api_request":
            self.start_execution_benchmark()
            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Calling API with the following parameters: {parameters}",
                    color=LogType.INFO,
                )
            try:
                function_response = await self._send_api_request(parameters)
            except APIRequestError("Function response failed", max_retries=self.max_retries, request_timeout=self.request_timeout, retry_delay=self.retry_delay) as e:
                await self.printr.print_async(
                    f"Error occurred during API request: {str(e)}",
                    color=LogType.ERROR,
                )
                e.log_error()  # Log the error details
                if e.retry_request():  # Retry the API request
                    try:
                        function_response = await self._send_api_request(parameters)
                    except APIRequestError("Function response failed", max_retries=self.max_retries, request_timeout=self.request_timeout, retry_delay=self.retry_delay) as retry_error:
                        await self.printr.print_async(
                            f"Retry failed: {str(retry_error)}",
                            color=LogType.ERROR,
                        )
                        raise
                else:
                    raise
            except:
                if self.settings.debug_mode:
                    await self.printr.print_async(
                        f"Unknown error with API call.",
                        color=LogType.INFO,
                    )

            if self.settings.debug_mode:
                await self.print_execution_time()

            if self.settings.debug_mode:
                await self.printr.print_async(
                    f"Response from API call: {function_response}",
                    color=LogType.INFO,
                )

        return function_response, instant_response

# Custom exception class to try to provide information about API errors.
# I am pretty sure this is mostly non-functional / broken right now and there should be another mechanism for retries in the code
class APIRequestError(Exception):
    """Custom exception for API request errors."""

    def __init__(self, message, status_code=None, response_body=None, max_retries=1, request_timeout=5, retry_delay=5):
        if status_code == 400:
            message = f"Bad Request: {message}"
        elif status_code == 401:
            message = f"Unauthorized: {message}"
        elif status_code == 404:
            message = f"Not Found: {message}"
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body
        self.retry_count = 0
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def log_error(self):
        """Custom error logging logic"""
        print(f"API Request Error: {self.args[0]}")
        print(f"Status Code: {self.status_code}")
        print(f"Response Body: {self.response_body}")

    def retry_request(self):
        """Custom retry logic with exponential backoff and jitter."""
        if self.retry_count < self.max_retries:
            self.retry_count += 1
            delay = self._calculate_retry_delay()
            print(f"Retrying the API request (Attempt {self.retry_count}/{self.max_retries})...")
            print(f"Waiting for {delay:.2f} seconds before retrying...")
            time.sleep(delay)
            return True
        else:
            print("Maximum retry attempts reached. Unable to complete the request.")
            return False

    def _calculate_retry_delay(self):
        """Calculate the retry delay using exponential backoff with jitter."""
        exponential_delay = self.retry_delay * (2 ** (self.retry_count - 1))
        jitter = random.uniform(0, 0.1 * exponential_delay)
        return exponential_delay + jitter