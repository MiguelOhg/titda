import { sendForm } from "./request.js";

export class Goal {
  constructor() {
    this.allGoalCards = document.querySelectorAll(".goal-card");
    console.log(this.allGoalCards);
    this.activateCreateForm();
    this.activateAllControls();
  }

  activateCreateForm() {
    const goalForm = document.querySelector(".goal-create-card form");
    new CreateGoalForm(goalForm);
  }

  activateAllControls() {
    this.allGoalCards.forEach((goalCard) => {
      new GoalControl(goalCard);
    });
  }
}

class CreateGoalForm {
  constructor(el) {
    this.form = el;
    this.createButton = el.querySelector("button[data-action='create-goal']");
    this.createButton.addEventListener(
      "click",
      this.handleCreateClick.bind(this)
    );
  }

  handleCreateClick(event) {
    event.preventDefault();
    sendForm(this.form, "POST", "/api/goal", this.addGoalToList);
    this.form.reset();
  }

  addGoalToList(rawData) {
    const data = JSON.parse(rawData);

    const goalCard = document.querySelector(".goal-card").cloneNode(true);
    const goalContent = goalCard.querySelector(".goal-content");

    const goalName = goalContent.querySelector("[data-goal-name]");
    goalName.textContent = data.name;
    goalName.setAttribute("data-goal-name", data.name);

    const goalDescription = goalContent.querySelector("[data-goal-description]");
    goalDescription.textContent = data.description;
    goalDescription.setAttribute("data-goal-description", data.description);

    new GoalControl(goalCard);
    goalCard.setAttribute("data-goal-id", data.id);
    document.querySelector(".goal-list").appendChild(goalCard);
  }
}

class GoalControl {
  constructor(goalCard) {
    this.goalCard = goalCard;
    this.goalElement = this.goalCard.querySelector(".goal-content");
    this.goalControl = this.goalCard.querySelector(".goal-control");
    this.goalID = this.goalCard.getAttribute("data-goal-id");
    this.form = this.goalCard.querySelector("form");

    this.editBtn = this.goalCard.querySelector(".toggle-control");
    this.editBtn.addEventListener("click", this.handleEditClick.bind(this));
    this.cancelBtn = this.goalCard.querySelector("[data-action='cancel']");
    this.cancelBtn.addEventListener(
      "click",
      this.handleCancelClick.bind(this)
    );
    this.deleteBtn = this.goalCard.querySelector("[data-action='delete']");
    this.deleteBtn.addEventListener(
      "click",
      this.handleDeleteClick.bind(this)
    );
    this.updateBtn = this.goalCard.querySelector("[data-action='update']");
    this.updateBtn.addEventListener(
      "click",
      this.handleUpdateClick.bind(this)
    );

    this.fillControlForm();
  }

  handleEditClick(event) {
    event.preventDefault();
    this.goalCard
      .querySelector(".goal-control-card")
      .classList.add("editing");
    this.goalElement.classList.add("d-none");
    this.editBtn.classList.add("d-none");
    this.goalControl.classList.remove("d-none");
  }

  handleCancelClick(event) {
    event.preventDefault();
    this.goalCard
      .querySelector(".goal-control-card")
      .classList.remove("editing");
    this.goalElement.classList.remove("d-none");
    this.editBtn.classList.remove("d-none");
    this.goalControl.classList.add("d-none");
  }

  handleDeleteClick(event) {
    event.preventDefault();
    if (window.confirm("Do you really want to remove this goal?")) {
        const endpoint = "/api/goal/" + this.goalID;
        sendForm(this.form, "DELETE", endpoint, (data, inputForm) => {
          let goalCard = inputForm.closest(".goal-card");
           goalCard.remove();
        });
     }
  }

  handleUpdateClick(event) {
    event.preventDefault();
    const endpoint = "/api/goal/" + this.goalID;
    sendForm(this.form, "PUT", endpoint, this.updateGoalInList);
    this.cancelBtn.click();
  }

  updateGoalInList(rawData, inputForm) {
    const data = JSON.parse(rawData);
    const goalCard = inputForm.closest(".goal-card");

    const goalName = goalCard.querySelector("[data-goal-name]");
    goalName.textContent = data.name;
    goalName.setAttribute("data-goal-name", data.name);

    const goalDescription = goalCard.querySelector("[data-goal-description]");
    goalDescription.textContent = data.description;
    goalDescription.setAttribute("data-goal-description", data.description);
  }

  fillControlForm() {
    const goalName = this.goalElement.querySelector(
      "[data-goal-name]"
    ).textContent;
    const goalDescription = this.goalElement.querySelector(
      "[data-goal-description]"
    ).textContent;
    this.form
      .querySelector("[name='id']")
      .setAttribute("value", this.goalID);
    this.form
      .querySelector("[name='name']")
      .setAttribute("value", goalName);
    this.form
      .querySelector("[name='description']")
      .setAttribute("value", goalDescription);
  }
}