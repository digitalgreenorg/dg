import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class GraphsService {
  
  private sampleURL = 'http://localhost:8000/training/sample_data';
  constructor(private http: Http) { }

  /*getDatas(): Promise<Data[]> {
    return this.http.get(this.sampleURL)
        .toPromise()
        .then(response => response.json() as Data[])
        .catch(this.handleError);
   }

   private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }*/

}
