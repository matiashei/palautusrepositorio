*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  pelle
    Set Password  pelle123
    Set Password Confirmation  pelle123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  pe
    Set Password  pelle123
    Set Password Confirmation  pelle123
    Click Button  Register
    Register Should Fail With Message  Minimum length of username is 3, minimum lenght of password is 8

Register With Valid Username And Too Short Password
    Set Username  pelle
    Set Password  p123
    Set Password Confirmation  p123
    Click Button  Register
    Register Should Fail With Message  Minimum length of username is 3, minimum lenght of password is 8

Register With Valid Username And Invalid Password
    Set Username  pelle
    Set Password  pelletest
    Set Password Confirmation  pelletest
    Click Button  Register
    Register Should Fail With Message  Password cannot consist of letters only

Register With Nonmatching Password And Password Confirmation
    Set Username  pelle
    Set Password  pelle123
    Set Password Confirmation  pelle654
    Click Button  Register
    Register Should Fail With Message  Passwords do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  pelle123
    Set Password Confirmation  pelle123
    Click Button  Register
    Register Should Fail With Message  User with username kalle already exists

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page