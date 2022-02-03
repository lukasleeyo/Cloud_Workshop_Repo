# Cloud_Workshop_Repo

[![Watch the video](images/Video.png)](https://www.youtube.com/watch?v=Pi8BmaV3f_M)

DSC Cloud Workshop was held on 22 Dec 2021 by Lee Jae Ho and Lee Jia Wei.

[Click here](https://github.com/GDSC-NUS/Cloud_Workshop_Repo) to view our repository.
- To try out our Toktik App, [here](https://tinyurl.com/TheToktikApp)!
  * But first, your email must be registered. Please contact [Lee Jae Ho](mailto:leejaeho1997@gmail.com) or [Lee Jia Wei](mailto:jiawei3e1@gmail.com)
- To read our slides, [here](https://tinyurl.com/DSCWorkshopCloudSlides)!
- To view participant's resources, [here](https://github.com/GDSC-NUS/Cloud_Workshop_Repo/tree/main/Participant%20Resources)!
- To check the codebase of our Toktik App on your environment, [here](https://github.com/GDSC-NUS/Cloud_Workshop_Repo/tree/main/Toktik%20Application)!

## Toktik App

1. Install python3 and pip. Using pip, install [streamlit](https://docs.streamlit.io/library/get-started/installation), [google-cloud-storage](https://pypi.org/project/google-cloud-storage/), and [google-cloud-firestore](https://pypi.org/project/google-cloud-firestore/).

2. Create a service account key in Google Cloud. Store this JSON key file in "Backend" folder. Then, in "Backend/initGCP.py", replace "#CREDENTIALS" with the JSON key file name. For more info, [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).

3. Set up Google Firestore and Storage as mentioned in the [workshop](https://www.youtube.com/watch?v=Pi8BmaV3f_M)

4. To run locally, enter in the terminal...
- "streamlit run toktik.py" to run the Toktik App
- "streamlit run dashboard.py" to visualize participant's activities
- "streamlit run cctv.py" to censor participant's posts
