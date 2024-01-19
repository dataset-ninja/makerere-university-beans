This **Makerere University Beans Image Dataset** was created to provide an open and accessible, well labeled, sufficiently curated image dataset. This is to enable researchers to build various machine learning experiments to aid innovations that may include; bean crop disease diagnosis and spatial analysis.

## Motivation

The dataset was created to provide an open, well-labelled, sufficiently curated and accessible beans image dataset. Data scientists, researchers, and the broader machine learning community can use the dataset for various machine learning experiments to build beans crop disease diagnosis and spatial analysis solutions. Despite the agricultural sector being a key focus for national economic development in Sub-Saharan Africa, crop pests and diseases, particularly affecting vital food security crops like beans, have posed significant challenges. A 2020 study conducted on bean rust in Uganda revealed that the disease led to estimated losses ranging from 5% to 67% across the six varieties examined. Similarly, a 2017 study on Angular Leaf Spot (ALS) in the Sub-Saharan African region demonstrated that ALS contributed to an alarming yield loss estimated at 384.2 tons per year for the entire region (Kijana et al., 2017).

The current trend in data collection and crop pest and disease diagnosis is transitioning from identifying diseases based on visible symptoms to employing data-driven solutions that leverage machine learning and computer vision techniques. Smallholder farmers and agricultural experts are now equipped with mobile phones loaded with software, enabling them to automatically collect field-level geo-coded and time-stamped data. Despite these advancements, the image data collected in the past has not been adequately curated and shared with the broader machine learning community.

## Dataset Creation

The dataset was created by a team of scientists from the Makerere Artificial Intelligence Lab, Marconi Society Machine Learning Laboratory Lab, and the National Crops Resources Research Institute (NaCRRI) in active collaboration. NaCRRI is an institute of the National Agricultural Research Organization (NARO) in charge of crop research in Uganda. The dataset includes bean crop trifoliate images, each instance includes the trifoliate image accompanied by the image category, i.e., ***healthy***, ***bean rust***, angular leaf spot(***als***), and a group of attributes associated with the crops from which the image was taken. 

<img src="https://user-images.githubusercontent.com/120389559/298026849-00c0a31e-152b-40cc-b1e2-364ba260147a.png" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Beans Data Class Labels.</span>

The dataset consists of bean image crops spread collected across the different regions in Uganda. Data were collected by random sampling from the areas where bean crop farming is practiced; these areas were identified by the experts. A few samples were collected from the identified areas to generate a dataset that represents the overall bean farming in the country. Each instance includes a trifoliate image, accompanied with attributes; the crop ***variety***, plant ***age***, ***district***, ***subcounty*** and the ***date*** of image capture. Each instance is associated with a class label to assert whether or not it was taken from a diseased crop. There are no relationships between the different image instances in the dataset.

## Collection Process

The beans image data was collected using mobile phones from bean farmer gardens. The data was collected using the Adsurv application, which is a mobile application that enables crowdsourcing of crop disease data from farmers’ gardens. Android devices were available for data collection. Each device was configured
with Adsurv for a specific data collector. The overall data collection exercise was conducted by a team including researchers from the Makerere Artificial Intelligence research Lab, the Marconi Society Machine Learning Laboratory at Makerere University and agricultural experts from Legumes program at the National Crops Resources Research Institute and an agricultural extension worker. The time frame matches the creation time frame of the ***date*** associated with the instances. For quality assurance data cleaning was done taking into consideration the missing values, defective images, resolution of inconsistencies, and removal of outliers. During data collection process, the data collectors had to manually input some values for predefined attributes; for example, crop variety, however, some of these attributes changed. Some of the images were taken in the middle of the day which led to an overexposure defect as a result of too much light hitting the camera sensor. This affected the quality of the images making it difficult to see the disease symptoms. These images were preprocessed to minimize the overexposure defect.

<img src="https://user-images.githubusercontent.com/120389559/298027417-a478b366-a1c1-4331-a85f-02fc11ba038b.png" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">On the left is the trifoliate image after preprocessing, on the right is the original trifoliate image with the overexposure defect.</span>

Note, similar **Makerere University Beans Image Dataset** datasets are also available on the [DatasetNinja.com](https://datasetninja.com/):

- [The KaraAgro AI Maize Dataset](https://datasetninja.com/kara-agro-ai-maize)
- [The KaraAgroAI Cocoa Dataset](https://datasetninja.com/kara-agro-ai-cocoa)