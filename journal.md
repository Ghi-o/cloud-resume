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
