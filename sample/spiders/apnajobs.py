import scrapy


class ApnajobsSpider(scrapy.Spider):
    name = "apnajobs"
    allowed_domains = ["apna.co"]
    start_urls = ["https://apna.co/jobs/full_time-jobs"]

    def parse(self, response):
        job_links_data=response.xpath("//div[@class='styles__JobDetails-sc-1eqgvmq-1 koxkvV']/h3/a").xpath('@href').getall()
        count = 0
        for i in job_links_data:
            job_links_data[count] = f"https://apna.co/{i}"
            count=count+1

        for job_link in job_links_data:
            yield scrapy.Request(url=job_link, callback=self.parse_job)
    
    def parse_job(self, response):
        print(response.text)
        job_dict = {}
        title = response.xpath("//div[@class='styles__TitleOpeningContainer-sc-15yd6lj-13 vQfBh']/h1/text()").get()
        job_dict['title'] = title
        yield job_dict
