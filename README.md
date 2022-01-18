# GenderPrediction
Predict gender from name using MultinomialNB

## I. Single Prediction
### Request

***URL (GET)*** : http://0.0.0.0:8500/prediction

***Header***

| Property  | Type  | Description  |
| ------------ | ------------ | ------------ |
|  project | String  | Project code|
|  apikey | String  | Secret key |

***Request***

| Params  | Type  | Description  |
| ------------ | ------------ |------------ |
| name  | String  | Name |
| language  | String  | Language **(vi, en)** |



***Sample request***
```
http://0.0.0.0:8500/prediction?name=Dao Quoc Dat&language=vi
```

### Response

***Sample response***
```
{
  "code": 200,
  "data": {
    "gender": 1,
    "acc": 98.9457
  },
  "message": null,
  "status": "success"
}
```

## II. Multiple Prediction
### Request

***URL (POST)*** : http://0.0.0.0:8500/prediction

***Header***

| Property  | Type  | Description  |
| ------------ | ------------ | ------------ |
|  project | String  | Project code|
|  apikey | String  | Secret key |

***Request (JSON Body)*** 

| Params  | Type  | Description  |
| ------------ | ------------ |------------ |
| language | String  | Language **(vi, en)**|
| name | List String |  List names |



## Guideline
```
cd source
python run app.py   
```
