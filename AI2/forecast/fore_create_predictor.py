import boto3
import time

forecast = boto3.client('forecast')

for group in forecast.list_dataset_groups()['DatasetGroups']:
    if group['DatasetGroupName'] == 'MyGroup':
        break
group_arn = group['DatasetGroupArn']

predictor_arn = forecast.create_predictor(
    PredictorName='MyPredictor', ForecastHorizon=12,
    PerformAutoML=True,
    InputDataConfig={'DatasetGroupArn': group_arn},
    FeaturizationConfig={'ForecastFrequency': "M"})['PredictorArn']
print('predictor ARN:', predictor_arn)

start = time.time()
status = ''
while status not in ['ACTIVE', 'CREATE_FAILED']:
    status = forecast.describe_predictor(
        PredictorArn=predictor_arn)['Status']
    time.sleep(10)
    print('{:7.2f} {}'.format(time.time()-start, status))

forecast_arn = forecast.create_forecast(
    ForecastName='MyForecast',
    PredictorArn=predictor_arn)['ForecastArn']
print('forecast ARN:', forecast_arn)

start = time.time()
status = ''
while status not in ['ACTIVE', 'CREATE_FAILED']:
    status = forecast.describe_forecast(
        ForecastArn=forecast_arn)['Status']
    time.sleep(10)
    print('{:7.2f} {}'.format(time.time()-start, status))
