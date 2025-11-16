---

title: Wikidata Editing for Authors and Books — A Structured Guide Based on Our Discussion
conversation: https://chatgpt.com/c/6910e063-b588-8331-b5d8-924e365f12b7

---

## **1. Introduction: What You’re Trying to Do**

### **1.1. Your actual goals**

* Build a workflow to edit and create Wikidata items related to **authors**, **books**, **translators**, and **public domain tracking**.
* Learn how to:

  * edit existing items correctly
  * create items when none exist
  * use references properly
  * understand recognition pathways inside Wikidata
  * evaluate whether a Toolforge project (Latin American public domain works database) is valid
* Avoid Wikipedia editing and focus solely on Wikidata.

### **1.2. Why Wikidata works for this use case**

* Bibliographic data fits well into structured statements.
* Useful for large-scale queries and public-domain automation.
* Community accepts users who contribute only to Wikidata.

---

## **2. Editing Without Using Wikipedia**

### **2.1. Can you grow as a Wikidata editor without touching Wikipedia?**

* Yes — we discussed that many respected contributors *only* edit Wikidata.
* Recognition is slower but absolutely possible.
* Your path is: consistent domain expertise + good modeling + high-quality references.

### **2.2. Why some people insist on Wikipedia edits**

* Cultural norm, not a rule.
* Wikipedia edits are more visible → people conflate visibility with contribution.
* Wikidata-only contributors are common but less “seen.”

---

## **3. The 9-Step Progression (Specific Version From Our Conversation)**

### **3.1. Short summary (what you requested)**

1. **Start with tiny edits** to existing items (dates, occupations, identifiers).
2. **Learn data models** for authors, books, works, editions.
3. **Work on “deep edits”**: filling missing fields, adding translators, adding references.
4. **Practice in Sandbox**, including how to add properties, qualifiers, references.
5. **Learn when to create new items**, and model them correctly.
6. **Add high-quality references**, including books, Google Books, and authority records.
7. **Add external identifiers** (VIAF, ISNI, Library of Congress), which raise the quality of your edits.
8. **Engage with WikiProjects** (Books, Latin America, Public Domain).
9. **Optional but powerful:** create queries and tools → recognition in the community.

### **3.2. Does this pathway include measures for “gaining recognition”?**

* Yes: steps 7–9 are specifically about visibility and value within the community.

---

## **4. Sandbox Editing (Based on Your Question “How do I edit items in the sandbox?”)**

### **4.1. What the sandbox is for**

* Practice adding:

  * statements
  * qualifiers
  * references
  * external IDs

### **4.2. How to add things**

* Same UI as real items.
* No restrictions; you can experiment with authors, books, and translators.

### **4.3. What we discussed about “no match available”**

* If a value for a property (e.g., *notable work*) does not exist:

  * use “string value” **only if temporary**
  * OR create the missing item
  * OR leave it blank until the item is created
* Best practice in bibliographic data: **create the missing item.**

---

## **5. Creating New Items (Specific to Authors, per your request)**

### **5.1. Steps we discussed**

1. **Search thoroughly** (names, aliases, nationalities, external identifiers).
2. If no match: **create a new item**.
3. Add core statements:

   * instance of → *human*
   * date/place of birth (if known)
   * date/place of death (if relevant to public domain purposes)
   * nationality
   * occupation → *writer*, *poet*, etc.
4. Add *notable works* ONLY if the book items exist or will be created.
5. Add identifiers (VIAF, ISNI, etc.).
6. Add references.

### **5.2. We emphasized:**

* Keep the initial item minimal but solid.
* You can always expand it later.

---

## **6. Adding References (Based on Your Direct Questions)**

### **6.1. If your reference is a book *not* in Wikidata**

We discussed:

* You **can** use a Google Books URL as reference.
* Better: use a stable library catalog (WorldCat, national library).
* Best: create a minimal book item and reference it with *stated in → the book*.

### **6.2. If the book *exists* in Wikidata**

* Yes, you **can** use the book itself as the reference.
* This is allowed if your data comes from title page, colophon, bibliography, etc.

### **6.3. Missing translator info (your specific question)**

* If translator is missing:

  * Add translator as a **new entity** (person).
  * Use:

    * property: **translator** (P655) on the *edition* item
  * Reference the edition’s title page using:

    * *stated in → the edition item*
    * *page(s)* qualifier optional.

---

## **7. Toolforge (Based on Your Project Idea and Concerns)**

### **7.1. Your proposed tool**

“Automatically generate a Latin American public domain works database, listing authors by nationality and years after their death to determine PD status.”

### **7.2. Our conclusion**

* This is **absolutely valid** as a Toolforge project.
* It benefits Wikidata and the wider Wikimedia ecosystem.
* It produces public domain awareness, which aligns with Wikimedia mission.

### **7.3. Why Toolforge usually enters the picture after ~1 year**

* Not a rule — just a typical community maturity curve:

  * You understand data models better
  * You know what tools are missing
  * You know the community’s needs
* BUT someone technically skilled (you) can start earlier.

---

## **8. Recognition Pathways in Wikidata (Specifically What You Asked About)**

### **8.1. What actually leads to community recognition**

* Consistent, accurate, referenced edits in a domain.
* Creating or improving data models (books/authors).
* Adding identifiers (big signal of quality).
* Building queries for others.
* Building **tools** (like your public-domain generator).
* Participating in WikiProjects (minimal but helpful).

### **8.2. What *doesn’t* matter much**

* You do **not** need Wikipedia edits.
* You do **not** need highly visible edits.
* You do **not** need talk page debates.