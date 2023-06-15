import { sendForm } from "./request.js";

export class Plan {
  constructor() {
    this.allPlanCards = document.querySelectorAll(".plan-card");
    console.log(this.allPlanCards);
    this.activateCreateForm();
    this.activateAllControls();
  }

  activateCreateForm() {
    const planForm = document.querySelector(".plan-create-card form");
    new CreatePlanForm(planForm);
  }

  activateAllControls() {
    this.allPlanCards.forEach((planCard) => {
      new PlanControl(planCard);
    });
  }
}

class CreatePlanForm {
  constructor(el) {
    this.form = el;
    this.createButton = el.querySelector("button[data-action='create-plan']");
    this.createButton.addEventListener(
      "click",
      this.handleCreateClick.bind(this)
    );
  }

  handleCreateClick(event) {
    event.preventDefault();

    sendForm(this.form, "POST", "/api/plan", this.addPlanToList);
    this.form.reset();
  }

  addPlanToList(rawData) {
    const data = JSON.parse(rawData);

    const planCard = document.querySelector(".plan-card").cloneNode(true);
    const planContent = planCard.querySelector(".plan-content");

    const planName = planContent.querySelector("[data-plan-name]");
    planName.textContent = data.name;
    planName.setAttribute("data-plan-name", data.name);

    const planLevel = planContent.querySelector("[data-plan-level]");
    planLevel.textContent = data.level;
    planLevel.setAttribute("data-plan-level", data.level);

    const planDescription = planContent.querySelector("[data-plan-description]");
    planDescription.textContent = data.description;
    planDescription.setAttribute("data-plan-description", data.description);

    new PlanControl(planCard);
    planCard.setAttribute("data-plan-id", data.id);

    document.querySelector(".plan-list").appendChild(planCard);
  }
}

class PlanControl {
  constructor(planCard) {
    this.planCard = planCard;
    this.planElement = this.planCard.querySelector(".plan-content");
    this.planControl = this.planCard.querySelector(".plan-control");
    this.planID = this.planCard.getAttribute("data-plan-id");
    this.form = this.planCard.querySelector("form");

    this.editBtn = this.planCard.querySelector(".toggle-control");
    this.editBtn.addEventListener("click", this.handleEditClick.bind(this));
    this.cancelBtn = this.planCard.querySelector("[data-action='cancel']");
    this.cancelBtn.addEventListener(
      "click",
      this.handleCancelClick.bind(this)
    );
    this.deleteBtn = this.planCard.querySelector("[data-action='delete']");
    this.deleteBtn.addEventListener(
      "click",
      this.handleDeleteClick.bind(this)
    );
    this.updateBtn = this.planCard.querySelector("[data-action='update']");
    this.updateBtn.addEventListener(
      "click",
      this.handleUpdateClick.bind(this)
    );

    this.fillControlForm();
  }

  handleEditClick(event) {
    event.preventDefault();
    this.planCard
      .querySelector(".plan-control-card")
      .classList.add("editing");
    this.planElement.classList.add("d-none");
    this.editBtn.classList.add("d-none");
    this.planControl.classList.remove("d-none");
  }

  handleCancelClick(event) {
    event.preventDefault();
    this.planCard
      .querySelector(".plan-control-card")
      .classList.remove("editing");
    this.planElement.classList.remove("d-none");
    this.editBtn.classList.remove("d-none");
    this.planControl.classList.add("d-none");
  }

  handleDeleteClick(event) {
    event.preventDefault();
    if (window.confirm("Do you really want to remove this plan?")) {
        const endpoint = "/api/plan/" + this.planID;
        sendForm(this.form, "DELETE", endpoint, (data, inputForm) => {
          let planCard = inputForm.closest(".plan-card");
           planCard.remove();
        });
     }
  }

  handleUpdateClick(event) {
    event.preventDefault();
    const endpoint = "/api/plan/" + this.planID;
    sendForm(this.form, "PUT", endpoint, this.updatePlanInList);
    this.cancelBtn.click();
  }

  updatePlanInList(rawData, inputForm) {
    const data = JSON.parse(rawData);
    const planCard = inputForm.closest(".plan-card");

    const planName = planCard.querySelector("[data-plan-name]");
    planName.textContent = data.name;
    planName.setAttribute("data-plan-name", data.name);

    const planDescription = planCard.querySelector("[data-plan-description]");
    planDescription.textContent = data.description;
    planDescription.setAttribute("data-plan-description", data.description);
  }

  fillControlForm() {
    const planName = this.planElement.querySelector(
      "[data-plan-name]"
    ).textContent;
    const planDescription = this.planElement.querySelector(
      "[data-plan-description]"
    ).textContent;
    this.form
      .querySelector("[name='id']")
      .setAttribute("value", this.planID);
    this.form
      .querySelector("[name='name']")
      .setAttribute("value", planName);
    this.form
      .querySelector("[name='description']")
      .setAttribute("value", planDescription);
  }
}