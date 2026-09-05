-- ? working on order.csv.

/* 
    our data contains orders data of three years: 2024 to 2026
*/
SELECT
    YEAR(order_date),
    COUNT(order_date)
FROM orders
GROUP BY YEAR(order_date)

/*
    in our business we are dealing with three types of customers: corporate,
    consumer, small business
*/
SELECT
    customer_segment
FROM orders
GROUP BY customer_segment

/*
    we have customers from 4 different regions: North America, Oceania, NULL, Europe.
    our customers are from these 6 countries: USA, Germany, United States, Australia,
    United Kingdom, Canada.
    our customers are from these 17 cities: Los Angeles, Montreal, Brisbane, London,
    New York, Houston, Sydney, Munich, Toronto, Birmingham, Hamburg, Vancouver, Chicago,
    Manchester, Berlin, Melbourne, NULL
    TODO : fix the NULL value in region. fix the countries semantic duplicate: USA, United States.
    TODO : fix the NULL value in the city.
*/
SELECT
    -- customer_region,
    -- customer_country
    customer_city
FROM orders
GROUP BY customer_city

/*
    in our dataset the order status columns contains 5 categories:
    Returned, Delivered, Cancelled, Processing, Shipped
*/
SELECT
    order_status
FROM orders
GROUP BY order_status

/*
    in our dataset the shipping method of the orders includes 4 methods:
    Economy, Standard, Express, Same Day
*/
SELECT
    shipping_method
FROM orders
GROUP BY shipping_method

/*
    the delivery status contains these 6 categories:
    Not Shipped, Returned, Delayed, In Transit, On Time, NULL
    TODO : delivery status contains NULL values that needs to be handled.
*/
SELECT
    delivery_status
FROM orders
GROUP BY delivery_status

/*
    payment status includes 4 categories: Paid, Pending, Failed, Refunded
    payment method: Bank Transfer, DEBIT CARD, Gift Card, Credit Card,
    PayPal, NULL
    TODO : payment method column includes NULL values, handle them.
*/
SELECT
    payment_method
    -- payment_status
FROM orders
GROUP BY payment_method

/*
    sales channel includes 4 ways: Website, Mobile App, Marketplace, Social Media

    customer acquisition channel columns includes 6 different categories:
    Organic Search, Paid Ads, Social Media, Referral, Email Marketing, Direct

    there are 6 different campagins in our dataset and a NULL value for the
    campaign type, most of the orders are not in a campaign duration.
    6 different types of campaigns are: SPRING_LAUNCH25, LOYALTY_REWARDS,
    BLACKFRIDAY25, SUMMER_SALE24, BLACKFRIDAY24, WINTER_CLEAROUT

    * A potential insight could be that we can see signs of this fact that the
    * number of sales in 2025 campaigns is higher that 2024 campaigns. By
    * Comparing BLACKFRIDAY25 & BLACKFRIDAY24 we can see in the BLACKFRIDAY25 we
    * submit more orders than BLACKFRIDAY24.
*/
SELECT
    campaign,
    COUNT(campaign) AS number_of_rows
    -- sales_channel
    -- customer_acquisition_channel,
FROM orders
GROUP BY campaign
