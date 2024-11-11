## Description

This project performs web scraping to gather and monitor the lowest product prices over the past month. It leverages a mix of modern technologies for data collection, storage, task scheduling, and email notifications. The project uses **Scrapy** to collect the data, and other AWS services like **Zappa**, **Flask**, **DynamoDB**, **SNS**, and **Scrapfly** to handle the infrastructure and notifications.

## Technologies Used

- **Scrapy**: Framework used for web scraping.
- **Zappa**: To deploy and manage the Flask application on AWS Lambda.
- **Flask**: Web framework used to build the API and manage routes.
- **DynamoDB**: AWS NoSQL database used to store the scraped data.
- **Schedulers**: A mechanism to schedule automatic scraping tasks.
- **SNS (Simple Notification Service)**: AWS service used to send email notifications with the results.
- **Scrapfly**: Service used to enhance and manage the web scraping process, bypassing restrictions like CAPTCHAs and IP bans.

## Prerequisites

Before using this application, you must have the following set up:

- A **DynamoDB table** called `products` with the product `id` as the **partition key**.
- The **ARN of an SNS topic** to send email notifications.

## Features

- **Scheduled Scraping**: Automatically collects price data from relevant websites.
- **Secure Storage**: Stores the data in DynamoDB for later analysis.
- **Automatic Notifications**: Sends summary emails with the lowest prices found using AWS SNS.
- **RESTful API**: Provides an interface for querying and managing collected data.


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/your-project.git
   cd your-project
2. Clone the repository:
   ```bash
   pip install -r requirements.txt

3. Set up the environment variables:
   ```bash
    export AWS
    export AWS_REGION
    export SCRAPFLY_API_KEY
    export SNS_ARN_TOPIC\
3. Set up the environment variables:
   ```bash
    zappa deploy prod
