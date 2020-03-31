import synapsepy as sp
from data import business_docs, beneficial_owner_docs

client = sp.Client(
    client_id='client_id_2bb1e412edd311e6bd04e285d6015267',
    client_secret='client_secret_6zZVr8biuqGkyo9IxMO5jY2QlSp0nmD4EBAgKcJW',
    fingerprint='e83cf6ddcf778e37bfe3d48fc78a6502062fc1030449628c699ef3c4ffa6f9a2000b8acc3c4c0addd8013285bb52c89e5267b628ca02fa84a6d71fe186b7cd5d',
    ip_address='127.0.0.1',
    devmode=True
)

print("****** DISCLAIMER: This script DOES NOT perform any validation, please make sure the values you enter are correct. Otherwise it will fail. ******\n")

#'5e7bedbe9f1eef0092a3b3f9'

user_id = input("User ID: ")
number_of_other_documents = input("Number of 'Other' Documents: ")
print("Enter y/n for to require the following KYC for the business")

ip = '127.0.0.1'
fingerprint = 'e83cf6ddcf778e37bfe3d48fc78a6502062fc1030449628c699ef3c4ffa6f9a2000b8acc3c4c0addd8013285bb52c89e5267b628ca02fa84a6d71fe186b7cd5d'


user = client.get_user(
    user_id, ip=ip, fingerprint=fingerprint, full_dehydrate=True)

oauth_body = {
    "refresh_token": user.body["refresh_token"],
    "scope": [
        "USER|PATCH",
        "USER|GET",
        "NODES|POST",
        "NODES|GET",
        "NODE|GET",
        "NODE|PATCH",
        "NODE|DELETE",
        "TRANS|POST",
        "TRANS|GET",
        "TRAN|GET",
        "TRAN|PATCH",
        "TRAN|DELETE",
        "SUBNETS|GET",
        "SUBNETS|POST",
        "SUBNET|GET",
        "SUBNET|PATCH",
        "STATEMENTS|GET",
        "STATEMENT|GET",
        "STATEMENTS|POST"
    ]
}

user.oauth(oauth_body)

business_response = user.update_info(business_docs)
owner_response = user.update_info(beneficial_owner_docs)

ubo_docs = {
    "entity_info": {
        "cryptocurrency": True,
        "msb": {
            "federal": True,
            "states": [
                "AL"
            ]
        },
        "public_company": False,
        "majority_owned_by_listed": False,
        "registered_SEC": False,
        "regulated_financial": False,
        "gambling": False,
        "document_id": owner_response["documents"][0]["id"]
    },
    "signer": {
        "document_id": owner_response["documents"][1]["id"],
        "relationship_to_entity": "CEO"
    },
    "compliance_contact": {
        "document_id": owner_response["documents"][1]["id"],
        "relationship_to_entity": "CEO"
    },
    "primary_controlling_contact": {
        "document_id": owner_response["documents"][1]["id"],
        "relationship_to_entity": "CEO"
    },
    "owners": [
        {
            "document_id": owner_response["documents"][1]["id"],
            "title": "CEO",
            "ownership": 95
        }
    ]
}

response = user.create_ubo(ubo_docs)
print(response)

