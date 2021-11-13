import boto3

forecast = boto3.client('forecast')

for fc in forecast.list_forecasts()['Forecasts']:
    forecast_arn = fc['ForecastArn']
    print('forecast ARN:', forecast_arn)
    forecast.delete_forecast(ForecastArn=forecast_arn)

for predictor in forecast.list_predictors()['Predictors']:
    predictor_arn = predictor['PredictorArn']
    print('predictor ARN:', predictor_arn)
    forecast.delete_predictor(PredictorArn=predictor_arn)
