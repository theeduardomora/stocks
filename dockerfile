FROM python:3.9.18-slim-bullseye

ARG GITHUB_USER=theeduardomora
ARG GITHUB_EMAIL=theeduardomora@gmail.com

# Configure Git with credentials
RUN apt-get update && \
    apt-get install -y git && \
    git config --global user.name $GITHUB_USER && \ 
    git config --global user.email $GITHUB_EMAIL

# Clone or pull the Git repository (replace with your repository URL)
WORKDIR /app
RUN git clone https://theeduardomora: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@github.com/theeduardomora/stocks.git .

COPY . .
RUN pip install -r requirements.txt
CMD ["sh", "-c", "python ./stock_plots.py && sh git_commands.sh"]