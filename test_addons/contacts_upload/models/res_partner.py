from odoo import fields, models, api
from odoo.exceptions import UserError
import http.client, urllib.request, urllib.parse, urllib.error, base64
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os


class ResPartner(models.Model):
    _inherit ="res.partner"
    upload_file = fields.Binary(string='Upload file')
    file_name = fields.Char()
    key = os.environ.get('FR_KEY')
    endpoint = os.environ.get('FR_ENDPOINT')

    # headers = {
    # # Request headers
    # 'Content-Type': 'application/json',
    # 'Ocp-Apim-Subscription-Key': '{subscription key}',
    # }

    # params = urllib.parse.urlencode({
    #     # Request parameters
    #     'pages': '{string}',
    #     'locale': '{string}',
    #     'stringIndexType': 'textElements',
    #     'features': '{string}',
    #     'queryFields': '{array}',
    # })

    @api.onchange('upload_file')
    def contacts_upload(self):
        if self.upload_file:
            extension = self.file_name.split('.')[-1]
            if(extension not in ['jpg' ,'png']):
                raise UserError("file must be jpg or png")
            else:
                #region 

                print(self.endpoint )
                print(self.key )
                # document_analysis_client = DocumentAnalysisClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))
                # poller = document_analysis_client.begin_analyze_document("prebuilt-businessCard", image_data=self.upload_file, locale="en-US")
                # business_cards = poller.result()

                # for business_card in business_cards:
                #     print("Business Card:")
                #     for field, value in business_card.fields.items():
                #         print(f"{field}: {value.content}")

                #endregion

                #region Custom URL

                # endpoint = "YOUR_ENDPOINT"
                # subscription_key = "YOUR_API_KEY"

                # # Construct the URL for the business card analysis API
                # analyze_url = f"{endpoint}/formrecognizer/v2.1-preview.3/businessCards"

                # headers = {
                #     "Content-Type": "application/json",
                #     "Ocp-Apim-Subscription-Key": subscription_key,
                # }
                # data = {
                #     "source": self.upload_file,
                #     "sourceType": "base64",
                # }
                # response = requests.post(analyze_url, headers=headers, json=data)
                # analysis_result = response.json()

                # # Extracted information
                # if "fields" in analysis_result:
                #     fields = analysis_result["fields"]
                #     print("Extracted information:")
                #     for field, value in fields.items():
                #         print(f"{field}: {value['text']}")
                # else:
                #     print("No fields extracted.")

                #endregion

                #region No data file

                # try:
                #     conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
                #     conn.request("POST", "{endpoint}/formrecognizer/documentModels/prebuilt-businessCard:analyze?api-version=2023-07-31&%s" % self.params, "{body}", self.headers)
                #     response = conn.getresponse()
                #     data = response.read()
                #     print(data)
                #     conn.close()
                # except Exception as e:
                #     print("[Errno {0}] {1}".format(e.errno, e.strerror))

                #endregion

        return
