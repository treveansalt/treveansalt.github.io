# Daylight Battery Release for Home Assistant

This package adds a small, deliberate manual override for a home battery. It lets a household choose a whole-number amount of energy to release during the day, start the release, and stop it again. It is useful when cheap overnight charging has left energy in the battery and a sunny day or other expected generation makes some daytime export or household use preferable.

The package is designed for installations where **SolisAgileManager** controls a Solis inverter and uses **Octopus Agile** tariff data for its normal schedule. The manual release is an explicit, temporary override: stopping it clears the SolisAgileManager override so normal tariff automation can resume.

## Requirements

- Home Assistant with a SolisAgileManager instance reachable over HTTP.
- SolisAgileManager configured for the inverter and Octopus tariff/product.
- A numeric battery discharge/energy sensor (replace the example entity IDs in the package).
- A Home Assistant `rest_command` for the SolisAgileManager discharge and clear-overrides endpoints.

## Install

1. Copy `ha-package/daylight_battery_release.yaml` into your Home Assistant packages directory, or merge its helpers, scripts, and template sensor into your existing configuration.
2. Replace the example entity IDs and REST command names with the names used by your installation.
3. Add `dashboard-card.yaml` as a manual card on the chosen dashboard.
4. Check the configuration, reload helpers/templates, and test with a small release amount. Confirm that **Stop release** clears the override and leaves the normal SolisAgileManager schedule in control.

The package intentionally does not contain credentials, hostnames, inverter serials, or personal dashboard entities.

