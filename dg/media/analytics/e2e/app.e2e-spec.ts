import { AnalyticsPage } from './app.po';

describe('analytics App', () => {
  let page: AnalyticsPage;

  beforeEach(() => {
    page = new AnalyticsPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
