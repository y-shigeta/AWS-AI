import boto3

personalize = boto3.client('personalize')

for solution in personalize.list_solutions()['solutions']:
    solution_arn = solution['solutionArn']
    print('solution ARN:', solution_arn)
    personalize.delete_solution(solutionArn=solution_arn)
