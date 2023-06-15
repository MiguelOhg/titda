import { sendForm } from "./request.js";

export class Action {
  constructor() {
    this.allActionCards = document.querySelectorAll(".action-card");
    console.log(this.allActionCards);
    this.activateCreateForm();
    this.activateAllControls();
  }

  activateCreateForm() {
    const actionForm = document.querySelector(".action-create-card form");
    new CreateActionForm(actionForm);
  }

  activateAllControls() {
    this.allActionCards.forEach((actionCard) => {
      new ActionControl(actionCard);
    });
  }
}

class CreateActionForm {
  constructor(el) {
    this.form = el;
    this.createButton = el.querySelector("button[data-action='create-action']");

    console.log(this.createButton);

    this.createButton.addEventListener(
      "click",
      this.handleCreateClick.bind(this)
    );
  }

  handleCreateClick(event) {
    event.preventDefault();
    sendForm(this.form, "POST", "/api/action", this.addActionToList);
    this.form.reset();
  }

  addActionToList(rawData) {
    const data = JSON.parse(rawData);

    const actionCard = document.querySelector(".action-card").cloneNode(true);
    const actionContent = actionCard.querySelector(".action-content");

    const actionName = actionContent.querySelector("[data-action-name]");
    actionName.textContent = data.name;
    actionName.setAttribute("data-action-name", data.name);

    const actionDescription = actionContent.querySelector("[data-action-description]");
    actionDescription.textContent = data.description;
    actionDescription.setAttribute("data-action-description", data.description);

    new ActionControl(actionCard);
    actionCard.setAttribute("data-action-id", data.id);
    document.querySelector(".action-list").appendChild(actionCard);
  }
}

class ActionControl {
  constructor(actionCard) {
    this.actionCard = actionCard;
    this.actionElement = this.actionCard.querySelector(".action-content");
    this.actionControl = this.actionCard.querySelector(".action-control");
    this.actionID = this.actionCard.getAttribute("data-action-id");
    this.form = this.actionCard.querySelector("form");

    this.editBtn = this.actionCard.querySelector(".toggle-control");
    this.editBtn.addEventListener("click", this.handleEditClick.bind(this));
    this.cancelBtn = this.actionCard.querySelector("[data-action='cancel']");
    this.cancelBtn.addEventListener(
      "click",
      this.handleCancelClick.bind(this)
    );
    this.deleteBtn = this.actionCard.querySelector("[data-action='delete']");
    this.deleteBtn.addEventListener(
      "click",
      this.handleDeleteClick.bind(this)
    );
    this.updateBtn = this.actionCard.querySelector("[data-action='update']");
    this.updateBtn.addEventListener(
      "click",
      this.handleUpdateClick.bind(this)
    );

    this.fillControlForm();
  }

  handleEditClick(event) {
    event.preventDefault();
    this.actionCard
      .querySelector(".action-control-card")
      .classList.add("editing");
    this.actionElement.classList.add("d-none");
    this.editBtn.classList.add("d-none");
    this.actionControl.classList.remove("d-none");
  }

  handleCancelClick(event) {
    event.preventDefault();
    this.actionCard
      .querySelector(".action-control-card")
      .classList.remove("editing");
    this.actionElement.classList.remove("d-none");
    this.editBtn.classList.remove("d-none");
    this.actionControl.classList.add("d-none");
  }

  handleDeleteClick(event) {
    event.preventDefault();
    if (window.confirm("Do you really want to remove this action?")) {
        const endpoint = "/api/action/" + this.actionID;
        sendForm(this.form, "DELETE", endpoint, (data, inputForm) => {
          let actionCard = inputForm.closest(".action-card");
           actionCard.remove();
        });
     }
  }

  handleUpdateClick(event) {
    event.preventDefault();
    const endpoint = "/api/action/" + this.actionID;
    sendForm(this.form, "PUT", endpoint, this.updateActionInList);
    this.cancelBtn.click();
  }

  updateActionInList(rawData, inputForm) {
    const data = JSON.parse(rawData);
    const actionCard = inputForm.closest(".action-card");

    const actionName = actionCard.querySelector("[data-action-name]");
    actionName.textContent = data.name;
    actionName.setAttribute("data-action-name", data.name);

    const actionDescription = actionCard.querySelector("[data-action-description]");
    actionDescription.textContent = data.description;
    actionDescription.setAttribute("data-action-description", data.description);
  }

  fillControlForm() {
    const actionName = this.actionElement.querySelector(
      "[data-action-name]"
    ).textContent;
    const actionDescription = this.actionElement.querySelector(
      "[data-action-description]"
    ).textContent;
    this.form
      .querySelector("[name='id']")
      .setAttribute("value", this.actionID);
    this.form
      .querySelector("[name='name']")
      .setAttribute("value", actionName);
    this.form
      .querySelector("[name='description']")
      .setAttribute("value", actionDescription);
  }
}