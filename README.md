---
title: SENTest
emoji: 🌍
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 1.28.2
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

pip install -r requirements.txt
echo "export OPENAI_API_KEY='Your openai api key'" >> ~/.zsh
source ~/.zsh
echo "export HUGGINGHUB_API_KEY='Your huggingface api key'" >> ~/.zsh
source ~/.zsh
python -m streamlit run app.py
