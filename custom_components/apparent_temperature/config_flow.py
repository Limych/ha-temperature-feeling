"""Homeassistant Config Flow for integration."""

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import (
    ConfigFlowResult,
)
from homeassistant.helpers.selector import selector

from .const import DOMAIN

MANUAL_SETUP_SCHEMA = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Required("temperature"): selector(
            {"entity": {"domain": "sensor", "device_class": "temperature"}}
        ),
        vol.Required("humidity"): selector(
            {"entity": {"domain": "sensor", "device_class": "humidity"}}
        ),
        vol.Optional("wind_speed"): selector(
            {"entity": {"domain": "sensor", "device_class": "wind_speed"}}
        ),
    }
)

WEATHER_SETUP_SCHEMA = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Required("weather"): selector({"entity": {"domain": "weather"}}),
    }
)

CLIMATE_SETUP_SCHEMA = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Required("climate"): selector({"entity": {"domain": "climate"}}),
    }
)

USER_STEP_TYPE = "type"
USER_STEP_TYPE_MANUAL_OPTION = "type_manual"
USER_STEP_TYPE_WEATHER_OPTION = "type_weather"
USER_STEP_TYPE_CLIMATE_OPTION = "type_climate"

USER_STEP_SCHEMA = vol.Schema(
    {
        vol.Required(USER_STEP_TYPE): selector(
            {
                "select": {
                    "options": [
                        {
                            "value": USER_STEP_TYPE_MANUAL_OPTION,
                            "label": "Manual",
                        },
                        {
                            "value": USER_STEP_TYPE_WEATHER_OPTION,
                            "label": "Weather entity",
                        },
                        {
                            "value": USER_STEP_TYPE_CLIMATE_OPTION,
                            "label": "Climate entity",
                        },
                    ],
                    "mode": "list",
                }
            }
        )
    }
)


class ApparentTemperatureConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Set up integration."""
        errors: dict[str, str] = {}

        if user_input is not None:
            user_step_type = user_input[USER_STEP_TYPE]
            if user_step_type == USER_STEP_TYPE_MANUAL_OPTION:
                return await self.async_step_manual_config()

            if user_step_type == USER_STEP_TYPE_WEATHER_OPTION:
                return await self.async_step_weather_config()

            if user_step_type == USER_STEP_TYPE_CLIMATE_OPTION:
                return await self.async_step_climate_config()

            errors[USER_STEP_TYPE] = "Not supported"

        return self.async_show_form(
            step_id="user", data_schema=USER_STEP_SCHEMA, errors=errors
        )

    async def async_step_climate_config(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Set up integration for climate entity."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["name"],
                data=user_input,
            )

        return self.async_show_form(
            step_id="climate_config", data_schema=CLIMATE_SETUP_SCHEMA
        )

    async def async_step_weather_config(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Set up integration for weather entity."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["name"],
                data=user_input,
            )

        return self.async_show_form(
            step_id="weather_config", data_schema=WEATHER_SETUP_SCHEMA
        )

    async def async_step_manual_config(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Set up integration manually, using provided entities."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["name"],
                data=user_input,
            )

        return self.async_show_form(
            step_id="manual_config", data_schema=MANUAL_SETUP_SCHEMA
        )
