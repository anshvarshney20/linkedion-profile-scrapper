
from fastapi import FastAPI, HTTPException
from AnalyseUserCase import AnalyseUserCase
from PdfReadExtractAnalyse.EmbedTheAnalysedSummarizedCases import EmbedTheAnalysedSummarizedCases
from ApiServiceModel.APIRequestModels import SummaryModel, CompareClientCaseModel

embedTheAnalysedSummarizedCases = EmbedTheAnalysedSummarizedCases()
analyseUserCase = AnalyseUserCase([])
app = FastAPI()

@app.get("/")
def read_root():
    return {"success":True, "message" : "ACG GPT SERVICE"}

@app.get("/gpt")
def read_item():
    embedTheAnalysedSummarizedCases = EmbedTheAnalysedSummarizedCases()
    context = '''A storm brews in the tech world as NexaTech Innovations, a leader in quantum computing, alleges Dr. Raphael Martinez, their former Chief Research Officer, of pilfering critical intellectual property. 
    The controversy is anchored on two clandestine discussions: one during a breakthrough celebratory event and another amidst Dr. Martinez's contentious exit. The crux is whether these conversations granted him any rights to the revolutionary algorithms he later commercialized. The courtroom drama intensifies as the court endeavors to ascertain the validity of these whispered exchanges and ponders if certain confidential documents shared between Dr. Martinez and NexaTech's CEO, Clara Benson, might be shielded due to 
    their once close professional camaraderie. '''
    embedding = embedTheAnalysedSummarizedCases.create_emebedding_for_summary(context)
    analyseUserCase = AnalyseUserCase(context)
    analyseUserCase.analyse(embedding,0.3)


    

@app.post("/compare-client-case-against-existing")
def get_similar(case:CompareClientCaseModel):
    try:        
        resp = analyseUserCase.compare_client_case_against_existing(case.caseIdToCompareAgainst,case.clientCaseId,case.userId)
        return {"success":True, "message" : resp}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/get-similar-cases")
def get_similar(summary:SummaryModel):
    try:
        embedding = embedTheAnalysedSummarizedCases.create_emebedding_for_summary(summary.summary)
        resp = analyseUserCase.analyse(embedding,summary.similarity)
        return {"success":True, "message" : resp}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)

