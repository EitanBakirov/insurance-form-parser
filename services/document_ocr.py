from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult


def analyze_layout(file_object=None, url=None, endpoint=None, key=None):

    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    if url:
        # Use remote URL
        poller = client.begin_analyze_document(
            model_id="prebuilt-layout",
            analyze_request=AnalyzeDocumentRequest(url_source=url)
        )
    elif file_object:
        # Use file-like object (uploaded file)
        poller = client.begin_analyze_document( 
            model_id="prebuilt-layout",
            body=file_object
        )
    else:
        raise ValueError("Either 'file_object' or 'url' must be provided.")

    result: AnalyzeResult = poller.result()

    full_text = ""
    for page in result.pages:
        for line in page.lines:
            full_text += line.content + "\n"

    return result, full_text

