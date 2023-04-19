const puppeteer = require('puppeteer');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;


async function start() {
  const browser = await puppeteer.launch({
    headless: true,
    defaultViewport: false,
    userDataDir: "./tmp"
  });


  const csvWriter = createCsvWriter({
    path: 'Times.csv',
    header: [
      { id: 'title', title: 'Title' },
    ]
  });


  const data = [];


  for (let i = 1; i <= 5; i++) {
    const page = await browser.newPage();
    await page.goto(`https://apna.co/jobs/full_time-jobs?page=2=${i}`);
    await page.screenshot({ path: 'Times.png' });
    const dataHandles = await page.$$('.styles__JobDetails-sc-1eqgvmq-1');


    for (const datahandle of dataHandles) {
      try {
        const title = await page.evaluate(el => el.innerText, datahandle);
        data.push({ title: title });
      } catch (error) { }
    }


    await page.close();
  }


  await csvWriter.writeRecords(data);
  console.log('CSV file written successfully');
  await browser.close();
}


start();