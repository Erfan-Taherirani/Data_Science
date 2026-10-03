# Feature Engineering

## Aggregate Usage Features

- total_minutes
- total_calls
- total_charge

## Call Intesity Features

- avg_day_minutes_per_call
- avg_eve_minutes_per_call
- avg_night_minutes_per_call
- avg_intl_minutes_per_call

## Usage Composition / Share Features

- day_minutes_share
- eve_minutes_share
- night_minutes_share
- intl_minutes_share

## Customer Service Features

- high_service_calls -> binary (x > 4)

## Interaction Features

- international_plan_service_risk -> intl_plan=True, customer_service_calls > 4

- high_usage_service_risk -> total_day_minutes > mean, customer_service_calls > 4

- intl_plan_no_vmail -> intl_plan=True, vmail=False

## Charge-efficiency features

- day_charge_per_minute
- eve_charge_per_minute
- night_charge_per_minute
- intl_charge_per_minute

## Voicemail Utilization

- has_vmail_usage -> number_vmail_messages > 0
- vmail_plan_unused -> vmail_plan=True, number_vmail_messages=0

## Account-length Transformations

- new_customer
- long_tenure

