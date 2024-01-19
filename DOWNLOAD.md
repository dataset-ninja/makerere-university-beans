Dataset **Makerere University Beans** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/t/l/qM/KGsuTnWUq34HAp7hqoVehLOkT9zWW5sJX3kH10IVYDafCfNcOJtSQYo6dMrl5ckFPKFOhyN3mO8ScFPUNY0s5Ykk87ZiqbyeOLqMwfLOCl6Qg9LLkReFDOWREwZP.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Makerere University Beans', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/TCKVEW#).