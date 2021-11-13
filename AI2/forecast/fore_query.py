import boto3
import sys

if len(sys.argv) != 2:
    print('python', sys.argv[0], 'item-id')
    exit()

forecast = boto3.client('forecast')
forecast_query = boto3.client('forecastquery')

for fc in forecast.list_forecasts()['Forecasts']:
    if fc['ForecastName'] == 'MyForecast':
        break
forecast_arn = fc['ForecastArn']

result = forecast_query.query_forecast(
    ForecastArn=forecast_arn,
    Filters={'item_id': sys.argv[1]})
for prediction in result['Forecast']['Predictions']:
    print(prediction+':')
    for line in result['Forecast']['Predictions'][prediction]:
        print(line['Timestamp'], line['Value'])
    print()
