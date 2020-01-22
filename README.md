# AMEC
## v1.0.0
### Administrator, Management, and Employee Creation

This program is currently just a basic setup with allowing users to follow a basic blueprint for user creation and permission setting.

*(AMEC currently just works for **Linux**, but will be compatible with **Windows** in the futre.)*


**Each type has access to types below it, but none have access to types that are equals**
> 0 - Administrators
>> 1 - Management(Supervisors)
>>> 2 - Employees

## Now for the boring stuff...

AMEC is intended to create users, a publicly open directory, and assign permissions per the user-type chosen.

### Create Users

The program will ask for the *NAME* and *USER-TYPE* for each profile desired to be created.

Next, will create the users each to have BASH as the shell, with a home directory, and set up a temporary password.

### Public Directory

The public directory is created right inside of /home called *COMMUNITY_BOWL*.

*COMMUNITY_BOWL*'s intent is to make the directory available for each user to make files available to other users without allowing everyone to access each users files.

There is then a symbolic link placed on each users Desktop to allow for easy and safe file transference from one user to another via *COMMUNITY_BOWL*.

### Assign Permissions

Finally, AMEC will assign each user the permissions that belong to them based on the *USER-TYPE* assigned (this is the blueprint explained **above**).
