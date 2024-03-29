import synapsepy as sp
from data import business_docs, beneficial_owner_docs
from credentials import client_id, client_secret, fingerprint, ip

client = sp.Client(
    client_id=client_id,
    client_secret=client_secret,
    fingerprint=fingerprint,
    ip_address=ip,
    devmode=True
)

print("\n********************************************************************************")
print("*                                                                              *")
print("*  DISCLAIMER: This script DOES NOT perform any validation, please make sure   *")
print("*              the values you enter are correct. Otherwise it will fail.       *")
print("*                                                                              *")
print("********************************************************************************\n")

#'5e7bedbe9f1eef0092a3b3f9'

user_id = input("User ID: ")
# # number_of_other_documents = input("Number of 'Other' Documents: ")
# print("\nEnter y/n for the following KYC options (these documents are the required KYC for the PLATFORM under v3 controls)\n")
# aoi_doc = input("AOI_DOC: ").lower()
# bylaws_doc = input("BYLAWS_DOC: ").lower()
# print(aoi_doc, bylaws_doc)
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

