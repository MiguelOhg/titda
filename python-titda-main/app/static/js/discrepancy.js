import { sendForm } from "./request.js";

export class Discrepancy {
  constructor() {
    this.allDiscrepancyCards = document.querySelectorAll(".discrepancy-card");
    this.activateCreateForm();
    this.activateAllControls();
  }

  activateCreateForm() {
    const discrepancyForm = document.querySelector(".discrepancy-create-card form");
    new CreateDiscrepancyForm(discrepancyForm);
  }

  activateAllControls() {
    this.allDiscrepancyCards.forEach((discrepancyCard) => {
      new DiscrepancyControl(discrepancyCard);
    });
  }
}

class CreateDiscrepancyForm {
  constructor(el) {
    this.form = el;
    this.createButton = el.querySelector("button[data-action='create-discrepancy']");

    this.createButton.addEventListener(
      "click",
      this.handleCreateClick.bind(this)
    );
  }

  handleCreateClick(event) {
    event.preventDefault();
    sendForm(this.form, "POST", "/api/discrepancy", this.addDiscrepancyToList);
    this.form.reset();
  }

  addDiscrepancyToList(rawData) {
    const data = JSON.parse(rawData);

    const discrepancyCard = document.querySelector(".discrepancy-card").cloneNode(true);
    const discrepancyContent = discrepancyCard.querySelector(".discrepancy-content");

    const discrepancyDescription = discrepancyContent.querySelector("[data-discrepancy-description]");
    discrepancyDescription.textContent = data.description;
    discrepancyDescription.setAttribute("data-discrepancy-description", data.description);

    new DiscrepancyControl(discrepancyCard);
    discrepancyCard.setAttribute("data-discrepancy-id", data.id);
    document.querySelector(".discrepancy-list").appendChild(discrepancyCard);
  }
}

class DiscrepancyControl {
  constructor(discrepancyCard) {
    this.discrepancyCard = discrepancyCard;
    this.discrepancyElement = this.discrepancyCard.querySelector(".discrepancy-content");
    this.discrepancyControl = this.discrepancyCard.querySelector(".discrepancy-control");
    this.discrepancyID = this.discrepancyCard.getAttribute("data-discrepancy-id");
    this.form = this.discrepancyCard.querySelector("form");

    this.editBtn = this.discrepancyCard.querySelector(".toggle-control");
    this.editBtn.addEventListener("click", this.handleEditClick.bind(this));
    this.cancelBtn = this.discrepancyCard.querySelector("[data-discrepancy='cancel']");
    this.cancelBtn.addEventListener(
      "click",
      this.handleCancelClick.bind(this)
    );
    this.deleteBtn = this.discrepancyCard.querySelector("[data-discrepancy='delete']");
    this.deleteBtn.addEventListener(
      "click",
      this.handleDeleteClick.bind(this)
    );
    this.updateBtn = this.discrepancyCard.querySelector("[data-discrepancy='update']");
    this.updateBtn.addEventListener(
      "click",
      this.handleUpdateClick.bind(this)
    );

    this.fillControlForm();
  }

  handleEditClick(event) {
    event.preventDefault();
    this.discrepancyCard
      .querySelector(".discrepancy-control-card")
      .classList.add("editing");
    this.discrepancyElement.classList.add("d-none");
    this.editBtn.classList.add("d-none");
    this.discrepancyControl.classList.remove("d-none");
  }

  handleCancelClick(event) {
    event.preventDefault();
    this.discrepancyCard
      .querySelector(".discrepancy-control-card")
      .classList.remove("editing");
    this.discrepancyElement.classList.remove("d-none");
    this.editBtn.classList.remove("d-none");
    this.discrepancyControl.classList.add("d-none");
  }

  handleDeleteClick(event) {
    event.preventDefault();
    if (window.confirm("Do you really want to remove this discrepancy?")) {
        const endpoint = "/api/discrepancy/" + this.discrepancyID;
        sendForm(this.form, "DELETE", endpoint, (data, inputForm) => {
          let discrepancyCard = inputForm.closest(".discrepancy-card");
           discrepancyCard.remove();
        });
     }
  }

  handleUpdateClick(event) {
    event.preventDefault();
    const endpoint = "/api/discrepancy/" + this.discrepancyID;
    sendForm(this.form, "PUT", endpoint, this.updateDiscrepancyInList);
    this.cancelBtn.click();
  }

  updateDiscrepancyInList(rawData, inputForm) {
    const data = JSON.parse(rawData);
    const discrepancyCard = inputForm.closest(".discrepancy-card");

    const discrepancyDescription = discrepancyCard.querySelector("[data-discrepancy-description]");
    discrepancyDescription.textContent = data.description;
    discrepancyDescription.setAttribute("data-discrepancy-description", data.description);
  }

  fillControlForm() {
    const discrepancyDescription = this.discrepancyElement.querySelector(
      "[data-discrepancy-description]"
    ).textContent;
    this.form
      .querySelector("[name='id']")
      .setAttribute("value", this.discrepancyID);
    this.form
      .querySelector("[name='description']")
      .setAttribute("value", discrepancyDescription);
  }
}