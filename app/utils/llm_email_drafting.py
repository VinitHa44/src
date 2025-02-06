from transformers import pipeline

def generate_email_body(complaint):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    issue_summary = summarizer(complaint.issue, max_length=15, min_length=10, do_sample=False)[0]["summary_text"]

    return f"""
    Hello Admin and Seller,

    A Buyer (User ID: {complaint.user_id}) has reported an issue with their order.

    **Order ID:** {complaint.order_id}
    **Product ID:** {complaint.product_id}
    **Issue Summary:** {issue_summary}
    **Uploaded Image (if any):** {complaint.image_url}

    Please review and take necessary action.

    Best Regards,
    Customer Support Team
    """
