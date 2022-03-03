#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    secret = {
        "COUCH_URL": "https://a0f0b8c0-8cb1-4db9-ad9a-601deb21f958-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "hQRO4quEkJaBXuInpXy1D22U4mVZOOs1dKmYkqQAOe_z",
        "COUCH_USERNAME": "a0f0b8c0-8cb1-4db9-ad9a-601deb21f958-bluemix"
    }
    authenticator = IAMAuthenticator(secret["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(secret["COUCH_URL"])
    response = service.post_find(
        db='reviews',
        fields=["id", "name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model", "car_year"],
        selector={'dealership': {'$eq': int(dict["id"])}},
    ).get_result()
    
    try:
        # result_by_filter=my_database.get_query_result(selector,raw_result=True)
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response['docs']}
        }
        return result
    
    except:
        return {
        'statusCode': 500,
        'message': 'Something went wrong on the server'
        }


