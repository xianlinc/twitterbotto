# TwitterBotto

## Breakdown of feature 3

3. * Notifies user when a selected followed account has a new account they follow. (Good for alpha as lots of notable accounts follow accounts or projects that they have freshly on their radar)
     * Notify User
       * Run checks automatically
       * If new accounts are detected send user a notification
         * Telegram bot to send user a notification
         * Server to host the program that is always running
     * Check if selected account is following a new account
       * Keep track of what accounts the selected account is following
       * Check who the account is currently following
       * Compare the two

## v1.1

#### Overview

This iteration should have a feature to check for new followers and display the new followers through a command line. The followers should also be saved in the database.

#### Features

**Check if selected account is following a new account**

* Keep track of what accounts the selected account is following
  * Use a database
* Check who the account is currently following
  * Query API
  * Update database if new followers
* Compare the two

**List out saved users from database**

* Typing list should list the handles of the users stored in the DB

**CLI based check function**

* Typing check should check for new followers and display them

**Relevant Links**

[Twitter Bot to check for new followers](https://gist.github.com/0a6e92911c206bb72232)

[Twitter Bot to automatically notify of a new follower on slack](https://gist.github.com/raspberrycoulis/f8e2b648479aa779074d1baccb235a35)

## v1.2 (coming soon)

#### Features



