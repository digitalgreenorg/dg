import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { TopBarDataComponent } from './top-bar-data/top-bar-data.component';
import { TopBarDataService } from './top-bar-data.service';
import { AccordionModule } from '../../node_modules/ngx-bootstrap';

@NgModule({
  declarations: [
    AppComponent,
    TopBarDataComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AccordionModule.forRoot(),
  ],
  providers: [TopBarDataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
