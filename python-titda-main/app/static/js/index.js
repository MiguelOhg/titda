import { Plan } from "./plan.js";
import { Action } from "./action.js";
import { Goal } from "./goal.js";
import { Discrepancy } from "./discrepancy.js";
import { DebugForm } from "./debug.js";

function main() {

  var urls = document.URL.split('/');

  if(urls[urls.length - 1] == 'actions'){
     new Action();
  } else if(urls[urls.length - 1] == 'goal') {
     new Goal();
  } else if(urls[urls.length - 1] == 'discrepancy') {
     new Discrepancy();
  } else if(urls[urls.length - 1] == 'plans') {
     new Plan();
  }


  if (document.querySelector(".debug-card")) {
    const debug = new DebugForm();
    debug.showResponse("");
  }
}

main();