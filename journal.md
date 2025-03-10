## Day 1: Deploying Resume Website

✅ What I Did:

- Converted resume to HTML/CSS.
- Deployed website on AWS S3.
- Updated Bucket Polcies
- Registered Domain in route 53.
- Requested TLS/SSL Certificate in ACM.
- Configured CloudFront for HTTPS.

⚠️ Challenges:

- Cloudfront not properly showing Content
- CloudFront giving access denied.

Solutions:

- Matching S3 bucket name to domain prevents misconfigurations with Route 53.
- Double check endpoints are pointed correectly in all services.

## Day 2: Deploying Resume in New S3 bucket.

✅ What I Did:

- Created new s3 bucket that matches domain name
- Created an alias record in Route 53 to s3 bucket route traffic
  Success!
- When [giokeels.com](http://giokeels.com) is searched, it goes to the bucket as it has public access.

Now I need to use HTTPS for security. Cloudfront and ACM will help with this.

- Go to ACM and request a TLS/SSL Certificate - **a digital certificate that verifies a website's identity and encrypts data sent between a browser and a website**. This helps protect users' information and establishes trust between users and websites

Now I will create a CloudFront distribution to use the Certificate for DNS validation

- I could have included Web Application Firewall (WAF) for increased security, but I'll keep it simple for cost sake.
- Once distribution is created with correct settings, update A record in Route 53 to point to CloudFront.
- SUCCESS!
- I can access my website through a cloudfront distribution over HTTPS.

📌 Key Lessons Learned:

**Match Your S3 Bucket Name to Your Domain** – Ensures smooth integration with Route 53.

**ACM Certificates Must Be in us-east-1 for CloudFront** – Regional mismatches cause issues.

**Use CloudFront for HTTPS & Performance** – Improved global availability with caching.

**Route 53 Directs Traffic, CloudFront Secures It** – Combining them correctly is key.

## Day 3: Building the serverless API.

I now will create a vistor counter that will be stored in a database(DynamoDB).

In DynamoDB:

- Created a table named visitor counter.
- Add a visits item to table.

I now will have to set up a lamdba function to read and update from the DynamoDB table.

In Lambda:

- Name function updateVisitorCount
- Now create actual python function to initialize DynamoDB table; with the help of ChatGPT and Amazon Q,and AWS Boto3 documentation as i am not proficient in coding, but can read and understand what is happening.
- test Code to make sure it can communicate with DynamoDb

i got an Access denied error message so i now need to update permissions to function

- Use DynamoDBFullaccess policy attached to Role
- I now have access

But now I have received another error code while testing, "Object of type decimal is not JSON serializable"

- I learned that DynamoDb stores numbers as decimal objects but JSON does not support Decimal.
- I need to update the function to convert decimal into int.
  if isinstance(visit_count, Decimal):
  visit_count = int(visit_count)

---

        import json
        import boto3
        from decimal import Decimal

        # Initialize DynamoDB resource

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('visitor-counter')

        def lambda_handler(event, context):
        try: # Retrieve the current visitor count

        response = table.get_item(Key={'id': 'visits'})
        # Get the current count or default to 0 if no record exists
        visit_count = response.get('Item', {}).get('count', 0)

        # Ensure count is an integer (fix Decimal issue)
        if isinstance(visit_count, Decimal):
            visit_count = int(visit_count)

        # Increment the visitor count
        visit_count += 1

        # Update the count in DynamoDB
        table.put_item(Item={'id': 'visits', 'count': visit_count})

        # Return the updated count as JSON (converted to int)
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            'body': json.dumps({'visitorCount': visit_count})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

SUCCESS! The Lambda function is now communicating with the DynamoDB table and is updating the visitor count.

### Creating API Gateway

- Create an API in AWS API Gateway
- Select REST API
- Name API - CloudResumeAPI
- create resource for visitor
- Integrate created lambda function into GET method
- Enable CORS on resource
- Deploy API and Test if Invoke URL comes back with correct code. make sure to add resource at the end of the invoke URL

SUCCESS! Now I need to connect API to my website.

### Connecting API to website

- Adding javascript code to index.html
  <p>Visitor Count: <span id="visitor-count">Loading...</span></p>  
   <script>
  async function fetchVisitorCount() {
  try {
  const response = await fetch("https://your-api-id.execute-api.us-west-1.amazonaws.com/prod/visitors");
  const data = await response.json();
  document.getElementById("visitor-count").textContent = data.visitorCount;
  } catch (error) {
  console.error("Error fetching visitor count:", error);
  document.getElementById("visitor-count").textContent = "Error";
  }
  }
  fetchVisitorCount();
  </script>

- ✅ Sends a GET request to your API Gateway.
- ✅ Waits for the response and converts it to JSON.
- ✅ Updates the webpage dynamically with the visitor count.
- ✅ Handles errors gracefully by showing "Error" instead of breaking the page.

NICE it works, now i will send update my S3 bucket with the code.

- PROBLEM: My new code was not updating, this was due to CloudFronts caching. SO i need to invalidate cache on the distribution.

SUCCESS! My website now shows a visitor count! LETS GOOOOOO
