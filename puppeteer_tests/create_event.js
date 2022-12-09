import puppeteer from "puppeteer";

(async () => {
  const event_name = "Test 3";

  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  page.setDefaultNavigationTimeout(0);

  await page.goto("http://127.0.0.1:8000");
  await page.waitForSelector("#id_username");

  // login
  await page.type("#id_username", "smokracek");
  await page.type("#id_password", "ilovebrooke");
  await page.click("#login-button");
  await page.waitForNavigation();

  // create event
  await page.goto("http://127.0.0.1:8000/create");
  await page.waitForSelector("#id_name");

  await page.type("#id_name", event_name);
  await page.type("#id_start", "10132023");
  await page.type("#id_description", "A party");
  await page.type("#id_address", "1126 N Catalina St");
  await page.type("#id_city", "Burbank");
  await page.type("#id_zip_code", "91505");
  await page.type("#id_apt", "0");
  await page.type("#id_state", "CA");
  await page.click("#next");
  await page.waitForSelector("#id_name");

  // add item
  await page.type("#id_name", "pasta");
  await page.type("#id_quantity", "5");
  await page.type("#id_description", "some pasta");
  await page.type("#id_price", "10");
  await page.click("#add");
  await page.waitForNavigation();
  await page.click("#finish");
  await page.waitForNavigation();

  async () => {
    const success = await page.evaluate(() => window.find(event_name));
    console.log(success ? "Successfully created event!" : "Error");
  };

  await browser.close();
})();
