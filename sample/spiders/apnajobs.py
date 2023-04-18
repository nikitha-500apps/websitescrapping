import scrapy


class ApnajobsSpider(scrapy.Spider):
    name = "apnajobs"
    allowed_domains = ["apna.co"]
    
    def start_requests(self):
          for page in range(1, 11):
                url = f"https://apna.co/jobs/full_time-jobs?page={page}"
          yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        job_links_data = response.xpath("//div[@class='styles__JobDetails-sc-1eqgvmq-1 koxkvV']/h3/a/@href").getall()
        count = 0
        for i in job_links_data:
            job_links_data[count] = f"https://apna.co/{i}"
            count += 1
        for job_link in job_links_data:
            yield scrapy.Request(url=job_link, callback=self.parse_job)

    def parse_job(self, response):
        job_dict = {}
        title = response.xpath("//div[@class='styles__TitleOpeningContainer-sc-15yd6lj-13 vQfBh']/h1/text()").get()
        job_dict['title'] = title
        company = response.xpath("//div[@class='styles__TextJobCompany-sc-15yd6lj-5 kIILUO']/text()").get()
        job_dict['company'] = company
        location = response.xpath("//div[@class='styles__TextJobArea-sc-15yd6lj-7 cHFGaJ']/text()").get()
        job_dict['location'] = location
        salary = response.xpath("//div[@class='styles__TextJobSalary-sc-15yd6lj-8 dGHiHv']/text()").get()
        job_dict['salary'] = salary
        job_requirements = response.xpath("//div[@class='styles__RequirementWrapper-d77mis-3 jfhEyQ']/p/text()").get()
        job_dict['job_requirements'] = job_requirements
        job_description = response.xpath("//div[@class='styles__DescriptionTextFull-sc-1532ppx-9 hKWjyK']/div/p/text()").get()
        job_dict['job_description'] = job_description
        yield job_dict