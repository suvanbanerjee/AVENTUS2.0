# PROJECT ζ (AVENTUS 2.0)

This project was build during the Aventus Hackathon 2024. The goal was to create a platform that allows users to create and share online ctf like challenges. This platform is build using flask and can be deployed on vercel.

## Features
- Create and share challenges
- Solve challenges
- Leaderboard
- User authentication
- Admin panel
- Certificate generation

## Tech Stack

- Flask
- Supabase
- React (Admin Panel)


## Testing
To test the project locally, you can run the following commands:
```bash
pip install -r requirements.txt
export SUPABASE_URL='some_url'
export SUPABASE_KEY='some_key'
python app.py
```

## Deployment

There is a vercel.json file in the project that allows you to deploy the project on vercel.This project will not work on free plan of vercel as the size of serverless functions is more than the limit of free plan. to deploy the project on vercel you have to disable the certificate generation feature.

## References

The main idea of the project was inspired by CTFd and the idea for levels was inspired by OverTheWire.
The textscrabble effect was taken from [here](https://codepen.io/soulwire/pen/mEMPrK) the home page ui is a modified version of an existing boostrap template that can be found [here](https://htmltemplates.co/) As pablo picasso said "Good artists copy, great artists steal" we want to thank the original creators of these resources.

## Contributors
Thanks to my friends without whom this project would not have been possible.
- Sharad
- Shreya
- Vaibhav