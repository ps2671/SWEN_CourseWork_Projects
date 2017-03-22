from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.contrib.auth.models import User, Group

from firstApp.forms import *
from firstApp.models import *
from django.db import models
from django.db.models import Count
import operator
import datetime


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                #password2=form.cleaned_data['password2'],
                email=form.cleaned_data['email']
            )

            userProfile=UserProfile(user=user,
                first_Name=form.cleaned_data['first_Name'],
                last_Name=form.cleaned_data['last_Name'],
                zipCode=form.cleaned_data['zipCode'],
                address=form.cleaned_data['address'],
                #notificationFrequency = form.cleaned_data['notificationFrequency'],
                pickupArrangements = form.cleaned_data['pickupArrangements'],
                date = form.cleaned_data['date'])

            user.save()
            userProfile.save()

            user_zipCode = form.cleaned_data['zipCode']
            user1 = form.cleaned_data['username']
            checkShZ = ShareZone.objects.filter(zipCode=form.cleaned_data['zipCode'])
            g = Group.objects.get(name='admin_user')
            d = Group.objects.get(name='basic_user')
            if not checkShZ:
                newShareZone = ShareZone.create(user_zipCode)
                shz = newShareZone
                userProfile.ShareZone = shz
                userProfile.request = True
                userProfile.is_admin = True
                userProfile.save()
                g.user_set.add(user)

            else:
                shz1 = checkShZ[0]
                userProfile.ShareZone = shz1
                user.is_active = False;
                userProfile.save()
                user.save()
                d.user_set.add(user)

            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'registration/register.html',
        variables,
    )

def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def home(request):
    userProfile = UserProfile.objects.get(user=request.user)
    Sharezone = ShareZone.objects.get(zipCode = userProfile.zipCode)
    community_shed = 'Does Not Exist'
    if Sharezone.has_CommunityShed == True:
        community_shed = Sharezone.CommunityShedLocation
        print('community_shed')
        print(community_shed)

    toolsRegister = ToolsRegister.objects.all()
    # get admin name for sharezone.
    admin = UserProfile.objects.all().filter(is_admin=True,zipCode=userProfile.zipCode).order_by('id')[0]
    print(admin)

    # get most recently added tools.
    recent_tools=[]

    all_tools = ToolsRegister.objects.all().order_by('-id')[:3]

    for tool in all_tools:
        if tool.userProfile.zipCode == userProfile.zipCode:
            recent_tools.append(tool)

    # get highest rated tools.
    highest_rated_tool_ids=[]
    tool_rate_dict = getHighestRatedTool(userProfile.zipCode)

    for tool_id,value in tool_rate_dict.items():
        highest_rated_tool_ids.append(tool_id)

    highest_rated_tools=ToolsRegister.objects.filter(pk__in=highest_rated_tool_ids)

    tools_rate={}
    for tool in highest_rated_tools:
        tools_rate[tool]= tool_rate_dict[tool.id]
    
    sorted_tools_rate = sorted(tools_rate.items(), key=operator.itemgetter(1),reverse=True)


    # get sharezone statistics
    no_of_users=0
    no_of_users = UserProfile.objects.filter(zipCode=userProfile.zipCode).count()
    borr_tool_ids = ToolRequest.objects.values('toolId')
    borr_tools = ToolsRegister.objects.filter(pk__in=borr_tool_ids)
    appr_tool_ids = ToolBorrowed.objects.values('toolId')
    appr_tools = ToolsRegister.objects.filter(pk__in=appr_tool_ids)
    
    no_of_tools=0
    shareZone_reg_tools=[]
    shareZone_borr_tools=[]
    shareZone_appr_tools=[]

    for tool in toolsRegister:
        if tool.userProfile.zipCode == userProfile.zipCode:
            shareZone_reg_tools.append(tool)

    for tool in borr_tools:
        if tool.userProfile.zipCode == userProfile.zipCode:
            shareZone_borr_tools.append(tool)

    for tool in appr_tools:
        if tool.userProfile.zipCode == userProfile.zipCode:
            shareZone_appr_tools.append(tool)

    no_of_tools = len(shareZone_reg_tools)
    no_of_tool_borrowed = len(shareZone_borr_tools)
    no_of_tool_approved = len(shareZone_appr_tools)

    admin_notification = adminNotification(userProfile)
    print('admin_notification')
    print(admin_notification)
    notification = checkRequest(userProfile)
    print('notification')
    print(notification)
    totalshz = getTotalNumberOfShareZones()
    totalusers = getTotalNumberOfUsers()
    totaltools = getTotalNumberOfToolsRegistered()

    variables = RequestContext(request, {
            'user': request.user, 'userPro': userProfile, 'admin_notification': admin_notification, 'notification': notification,'community_shed':community_shed,'recent_tools':recent_tools,'admin':admin,'highest_rated_tools':highest_rated_tools,'sorted_tools_rate':sorted_tools_rate,
            'no_of_users': no_of_users,
            'no_of_tools': no_of_tools,
            'no_of_tool_borrowed' : no_of_tool_borrowed,
            'no_of_tool_approved' : no_of_tool_approved,
            'totalshz': totalshz,
            'totalusers': totalusers,
            'totaltools': totaltools})
    context = {'user': request.user, 'userPro': userProfile,  'notification': notification,'community_shed':community_shed,'admin_notification':admin_notification}
    for object in toolsRegister:
        if object.userProfile_id == userProfile.id:
            variables['toolsRegister'] = toolsRegister
    return render_to_response(
        'home.html',
        variables
    )

@login_required
def adminNotification(userProfile):
    k = False
    users= UserProfile.objects.all().filter(zipCode=userProfile.zipCode)
    for object in users:
        if object.request == False:
            print(object)
            k = True
    return k

@login_required
def viewTool(request):
    userProfile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST' and 'View' in request.POST:
        tool_id = request.POST.get('rat_tool_id')
        print(tool_id)

        tool = ToolsRegister.objects.get(id=tool_id)
        admin_notification = adminNotification(userProfile)
        notification = checkRequest(userProfile)
        variables = RequestContext(request, {
            'user': request.user,
            'tool':tool,
            'notification':notification,
            'admin_notification':admin_notification
        })
        return render_to_response(
        'viewTool.html',
        variables
        )

@login_required
def showAllRecentTools(request):
    userProfile = UserProfile.objects.get(user=request.user)
    tools = ToolsRegister.objects.all().order_by('-id')
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    recent_tools=[]
    
    for tool in tools:
        if tool.userProfile.zipCode == userProfile.zipCode:
            recent_tools.append(tool)

    print(recent_tools)

    variables = RequestContext(request, {
            'user': request.user,
            'recent_tools':recent_tools,
            'notification':notification
        })
    return render_to_response(
        'showAllRecentTools.html',
        variables
    )

@login_required
def showAllHighRatedTools(request):

    userProfile = UserProfile.objects.get(user=request.user)
    # get highest rated tools.
    highest_rated_tool_ids=[]
    tool_rate_dict = getAllHighestRatedTool(userProfile.zipCode)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    for tool_id,value in tool_rate_dict.items():
        highest_rated_tool_ids.append(tool_id)

    highest_rated_tools=ToolsRegister.objects.filter(pk__in=highest_rated_tool_ids)

    tools_rate={}
    for tool in highest_rated_tools:
        tools_rate[tool]= tool_rate_dict[tool.id]
    
    sorted_tools_rate = sorted(tools_rate.items(), key=operator.itemgetter(1),reverse=True)

    variables = RequestContext(request, {
            'user': request.user,
            'notification':notification,
            'highest_rated_tools':highest_rated_tools,
            'sorted_tools_rate':sorted_tools_rate
        })
    return render_to_response(
        'showAllHighRatedTools.html',
        variables
    )

@login_required
def showAllMostActiveUsers(request):
    recent_added_tools = ToolsRegister.objects.all().order_by('-id')

    variables = RequestContext(request, {
            'user': request.user,
            'tools':tools
        })
    return render_to_response(
        'showAllMostActiveUsers.html',
        variables
    )

def changePasswordSuccess(request):
    return render_to_response('registration/changePasswordSuccess.html')

@login_required
def checkRequest(userProfile):
    #check in ToolRequest as tool owner and  in ToolBorrowed and ToolRejected as tool borrower
    k = False
    all_entries1 = ToolRequest.objects.all()
    for object in all_entries1:
        if ToolsRegister.objects.get(id=object.toolId_id).userProfile_id == userProfile.id and object.requestStatus == 0:
            k = True

    all_entries2 = ToolBorrowed.objects.all()
    for object in all_entries2:
        if object.borrowerId == userProfile.user.username and object.notified == False:
            k = True
            object.notified = True
            object.save()

    all_entries3 = ToolRejected.objects.all()
    for object in all_entries3:
        if object.requesterId == userProfile.user.username and object.notified == False:
            k = True
            object.notified = True
            object.save()

    return k

@login_required
def myProfile(request):
    user = request.user
    print(user)
    userProfile = UserProfile.objects.get(user=user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            userProfile.first_Name = form.cleaned_data['first_Name']
            userProfile.last_Name = form.cleaned_data['last_Name']
            userProfile.zipCode = form.cleaned_data['zipCode']
            userProfile.address = form.cleaned_data['address']
            userProfile.pickupArrangements = form.cleaned_data['pickupArrangements']
            userProfile.date = form.cleaned_data['date1']
            user.save()
            userProfile.save()
            variables = RequestContext(request, {
                'form': form
            })
            return HttpResponseRedirect('/home/')
    else:
        form = UserProfileForm()
        form.fields['username'].initial = user.username
        form.fields['email'].initial = user.email
        form.fields['first_Name'].initial =userProfile.first_Name
        form.fields['last_Name'].initial = userProfile.last_Name
        form.fields['zipCode'].initial = userProfile.zipCode
        form.fields['address'].initial = userProfile.address
        form.fields['pickupArrangements'].initial = userProfile.pickupArrangements
        form.fields['date1'].initial = userProfile.date
    return render_to_response('registration/myProfile.html',context_instance = RequestContext(request,
                               {'form': form, 'notification' : notification,'admin_notification':admin_notification}))

def changePassword(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    if request.method == 'POST' and 'change_Password' in request.POST:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return HttpResponseRedirect('/changePasswordSuccess/')
    else:
        form = ChangePasswordForm()
        variables = RequestContext(request, {
            'form': form})

    return render_to_response('registration/changePassword.html', context_instance=RequestContext(request,
                                                                                                {'form': form, 'notification' : notification,'admin_notification':admin_notification}))

@login_required
def myTools(request):
    userProfile = UserProfile.objects.get(user=request.user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    print (notification)
    context = {'user': request.user, 'notification': notification,'admin_notification':admin_notification}
    return render_to_response('ToolManagement/myTools.html',
                              context)

@login_required
def myRegisteredTools(request):
    userProfile = UserProfile.objects.get(user=request.user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    tool_info=ToolsRegister.objects.all()
    tool_data={
        'tool_detail':tool_info
    }
    try:
        context = {'userProfileId':userProfile.id,'notification': notification,'admin_notification':admin_notification}
        toolsRegister = ToolsRegister.objects.all()
        for object in toolsRegister:
            if object.userProfile_id == userProfile.id:
                context['toolsRegister'] = toolsRegister
        if request.method == 'POST' and 'changeActivation' in request.POST:
            if request.POST.get('IDForTheTool', False):
                ToolID = request.POST['IDForTheTool']
                toolsRegister_temp = ToolsRegister.objects.get(id=ToolID)
                if canUpdateTool(ToolID):
                    if toolsRegister_temp.statusOfTheTool == 'Available':
                        toolsRegister_temp.statusOfTheTool = 'Unavailable'
                    else:
                        toolsRegister_temp.statusOfTheTool = 'Available'
                    toolsRegister_temp.save()
                    return HttpResponseRedirect('/manageMyTools/')
                else:
                    cannot_update_tool=True
                    context['cannot_update_tool'] = cannot_update_tool
                    print("display the prompt that this tool can't be updated. either borrowed or pending request!")

        elif request.method == 'POST' and 'updateTool' in request.POST:
            if request.POST.get('IDForTheTool', False):
                ToolID = request.POST['IDForTheTool']
                if canUpdateTool(ToolID):
                    request.session['ToolId'] = ToolID
                    return HttpResponseRedirect('/toolUpdate/')
                else:
                    cannot_update_tool=True
                    context['cannot_update_tool'] = cannot_update_tool
                    print("display the prompt that this tool can't be updated. either borrowed or pending request!")

    except ObjectDoesNotExist:
        print("Need to show the user that they haven't created the tables till now.")
        # Need to have some functionality for this
    return render_to_response('ToolManagement/manageTheRegisteredTool.html',context_instance = RequestContext(request, context))

@login_required
def myToolUpdate(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    Sharezone = ShareZone.objects.get(zipCode = userProfile.zipCode)
    tool = ToolsRegister.objects.get(id=request.session['ToolId'])


    if request.method == 'POST':
        print(request.session['ToolId'])
        form = ToolUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            toolAvailChoice = form.cleaned_data['addressOfTheTool']
            if toolAvailChoice == 'Home':
                addressOfTheTool = userProfile.address
            else:
                if Sharezone.has_CommunityShed == True:
                    addressOfTheTool = Sharezone.CommunityShedLocation
                else:
                    addressOfTheTool = userProfile.address

            tool.addressOfTheTool = addressOfTheTool
            tool.statusOfTheTool = form.cleaned_data['statusOfTheTool']
            tool.categoryOfTheTool = form.cleaned_data['categoryOfTheTool']
            print(form.cleaned_data['image'])
            if form.cleaned_data['image'] != None :
                tool.image = form.cleaned_data['image']
            tool.conditionOfTheTool = form.cleaned_data['conditionOfTheTool']
            tool.toolDescription = form.cleaned_data['toolDescription']
            tool.save()
            # return HttpResponseRedirect('/manageMyTools/')
            return render_to_response('ToolManagement/successToolUpdate.html',context_instance = RequestContext(request,
                               {'alert': True,'succ_msg':'Tool Information Updated Successfully.','admin_notification':admin_notification,'Sharezone':Sharezone,'notification': notification}))
    else:
        form = ToolUpdateForm()
        form.fields['nameOfTheTool'].initial = tool.nameOfTheTool
        form.fields['addressOfTheTool'].initial = tool.addressOfTheTool
        form.fields['categoryOfTheTool'].initial =tool.categoryOfTheTool
        form.fields['conditionOfTheTool'].initial = tool.conditionOfTheTool
        form.fields['toolDescription'].initial = tool.toolDescription

    return render_to_response('ToolManagement/toolUpdate.html',context_instance = RequestContext(request,
                               {'form': form,'tool_image_url':tool.image.url,'Sharezone':Sharezone,'admin_notification':admin_notification,'notification': notification}))

def canUpdateTool(ToolID):
    toolRequest = ToolRequest.objects.all()
    k = False
    count = 0
    for tools in toolRequest:
        if tools.toolId_id == int(ToolID):
            count = count + 1
            if tools.requestStatus !=0 and tools.requestStatus != 1: #shouldn't be in pending or borrowed status
                k = True
    if count==0: #it checks that the given tool has not yet been requested so it won't be in toolrequest table which means it is eligible to be updated!
        k = True
    return k

def getTotalNumberOfUsers(): #for system admin
    count = -1
    userProfile = UserProfile.objects.all()
    for object in userProfile:
        count = count + 1
    return count

def getTotalNumberOfToolsRegistered(): #for system admin
    count = 0
    toolsRegistered = ToolsRegister.objects.all()
    for object in toolsRegistered:
        count = count + 1
    return count

def getTotalNumberOfShareZones(): #for system admin
    count = 0
    shareZone = ShareZone.objects.all()
    for object in shareZone:
        count = count + 1
    return count

#to call these methods
# count = getTotalNumberOfShareZones()

def getHighestRatedTool(zipCode):

    tool_rate={}
    toolRegisterd = ToolsRegister.objects.all()
    ShZU = UserProfile.objects.all().filter(zipCode=zipCode)

    #to get the list of tools that are in this sharezone
    toolsOnlyFromThisShZU = []
    for object in toolRegisterd:
        for object1 in ShZU:
            if object.userProfile_id == object1.id:
                toolsOnlyFromThisShZU.append(object.id)

    toolReturn = ToolReturn.objects.all()
    toolList = [] #list of toolId
    toolRating = [] #List of the rating

    count = 0
    for object in toolReturn:
        for object1 in toolsOnlyFromThisShZU:
            if object.toolId_id == object1:
                rating = int(object.rating)
                if count < 3: #this ensure it will return 3 tools
                    toolRating.append(rating)
                    toolList.append(object.toolId_id)
                    tool_rate[object.toolId_id]=rating
                else:
                    for n, i in enumerate(toolRating):
                        if rating >= i:
                            toolRating[n] = rating #Even if the rating are same, we will be adding fresh tool transactions.
                            toolList[n] = object.toolId_id
                            tool_rate[object.toolId_id]=rating
                count = count + 1
    return tool_rate

def getAllHighestRatedTool(zipCode):

    tool_rate={}
    toolRegisterd = ToolsRegister.objects.all()
    ShZU = UserProfile.objects.all().filter(zipCode=zipCode)

    #to get the list of tools that are in this sharezone
    toolsOnlyFromThisShZU = []
    for object in toolRegisterd:
        for object1 in ShZU:
            if object.userProfile_id == object1.id:
                toolsOnlyFromThisShZU.append(object.id)

    toolReturn = ToolReturn.objects.all()
    toolList = [] #list of toolId
    toolRating = [] #List of the rating

    count = 0
    for object in toolReturn:
        for object1 in toolsOnlyFromThisShZU:
            if object.toolId_id == object1:
                rating = int(object.rating)
                if count < 20: #this ensure it will return 3 tools
                    toolRating.append(rating)
                    toolList.append(object.toolId_id)
                    tool_rate[object.toolId_id]=rating
                else:
                    for n, i in enumerate(toolRating):
                        if rating >= i:
                            toolRating[n] = rating #Even if the rating are same, we will be adding fresh tool transactions.
                            toolList[n] = object.toolId_id
                            tool_rate[object.toolId_id]=rating
                count = count + 1
    return tool_rate

#to call this method:
#   toolList, toolRating = getHighestRatedTool()
#to get the toolID and/or rating
#   for n, i in enumerate(toolRating):
#       print(toolRating[n])
#       print(toolList[n])

@login_required
def myToolsRegistration(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    Sharezone = ShareZone.objects.get(zipCode = userProfile.zipCode)
    context = {'Sharezone': Sharezone}
    if request.method == 'POST' and 'submitTheTool' in request.POST:
        print("POST")
        form = ToolEntryForm(request.POST, request.FILES)
        if form.is_valid():
            print("POST Valid")
            toolAvailChoice=form.cleaned_data['addressOfTheTool']
            print('toolAvailChoice')
            print(toolAvailChoice)
            if toolAvailChoice == 'Home':
                addressOfTheTool = userProfile.address
            else:
                if Sharezone.has_CommunityShed == True:
                    addressOfTheTool = 'Shed'
                else:
                    addressOfTheTool = userProfile.address
            toolRegister = ToolsRegister(userProfile=userProfile,
                                         nameOfTheTool=form.cleaned_data['nameOfTheTool'],
                                         addressOfTheTool=addressOfTheTool,
                                         statusOfTheTool=form.cleaned_data['statusOfTheTool'],
                                         categoryOfTheTool=form.cleaned_data['categoryOfTheTool'],
                                         image=form.cleaned_data['image'],
                                         conditionOfTheTool=form.cleaned_data['conditionOfTheTool'],
                                         toolDescription=form.cleaned_data['toolDescription']
                                         )
            toolRegister.save()
        #return render_to_response('ToolManagement/successToolRegistration.html')
            return render_to_response('ToolManagement/successToolRegistration.html',context_instance = RequestContext(request,
                               {'alert': True,'succ_msg':'Tool Information saved Successfully.','Sharezone':Sharezone,'admin_notification':admin_notification,'notification': notification}))
    else:
        form = ToolEntryForm()
        context['form'] = form
        # variables = RequestContext(request, {
        # 'form': form })

    #return render_to_response('ToolManagement/addNewTool.html',RequestContext(request, {'form': form}),)
    return render_to_response('ToolManagement/addNewTool.html',context_instance = RequestContext(request,
                               {'form': form,'Sharezone':Sharezone,'notification': notification,'admin_notification':admin_notification}))

@login_required
def borrowTool(request):
    userProfile = UserProfile.objects.get(user=request.user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    zipcode = userProfile.zipCode
    cannot_borrow=False
    try:
        toolsRegister = ToolsRegister.objects.all()
        ShZU = UserProfile.objects.all().filter(zipCode=zipcode)
        toolRequest1 = ToolRequest.objects.all().filter(requester_id=userProfile.user.username)
        firstTime = True
        toolsOnPending = []
        i =1
        for object in toolRequest1:
            if object.requestStatus == 0:
                if firstTime:
                    toolsOnPending = [object.toolId_id]
                    firstTime = False
                else:
                    toolsOnPending.insert(i, object.toolId_id)
                    i = i + 1

        i = 1
        toolsWhichCanBeBorrowed = []
        for object in toolsRegister:
            for object1 in ShZU:
                    if object.userProfile_id == object1.id and object.userProfile_id != userProfile.id and object.statusOfTheTool == 'Available':
                        a = 0
                        for object2 in toolsOnPending:
                            if object2 == object.id:
                                a = 1
                        if a == 0:
                            toolsWhichCanBeBorrowed.insert(i, object)
                            i = i + 1

        context = {'userProfileId': userProfile.id,'notification':notification,'admin_notification':admin_notification}
        context['toolsRegister'] = toolsRegister
        context['ShZU'] = ShZU
        context['toolOnPending'] = toolsOnPending
        context['toolsWhichCanBeBorrowed'] = toolsWhichCanBeBorrowed

        if request.method == 'POST'and 'borrow' in request.POST:
            print('In borrow tool post')
            form = ToFromDateForm()
            ToolID = request.POST['IDForTheTool']
            print(ToolID)
            toolsRegister_temp = ToolsRegister.objects.get(id=ToolID)
            print(toolsRegister_temp.nameOfTheTool)
            context = {'userProfileId': userProfile.id,'notification':notification,'ToolID':ToolID,'toolsRegister_temp':toolsRegister_temp,'form':form}
            return render_to_response('ToolManagement/borrowTool.html',context_instance = RequestContext(request, {'userProfileId': userProfile.id,'notification':notification,'ToolID':ToolID,'toolsRegister_temp':toolsRegister_temp,'form':form,
                                        'cannot_borrow':cannot_borrow}))


        if request.method == 'POST' and 'requestToBorrow' in request.POST or 'CheckAvail' in request.POST:
            if request.POST.get('IDForTheTool', False):
                form = ToFromDateForm(request.POST)
                if form.is_valid():
                    ToolID = request.POST['IDForTheTool']
                    toolsRegister_temp = ToolsRegister.objects.get(id=ToolID)
                    toolsRegister_temp.requested=True
                    toolsRegister_temp.requester_id=userProfile.user.username
                    toolsRegister_temp.save()

                    tool_already_requested = ToolRequest.objects.all().filter(toolId=toolsRegister_temp,requestStatus=1)

                    print('tool_already_requested')
                    print(tool_already_requested)

                    if tool_already_requested:
                        for tool in tool_already_requested:
                            requestedFromDate=tool.requestedFromDate
                            print('requestedFromDate')
                            print(requestedFromDate)
                            requestedToDate=tool.requestedToDate
                            print('requestedToDate')
                            print(requestedToDate)

                            if requestedFromDate <= form.cleaned_data['fromDate'] <= requestedToDate:
                                print('cannot_borrow')
                                cannot_borrow=True
                                return render_to_response('ToolManagement/borrowTool.html',
                                    context_instance = RequestContext(request, 
                                        {'userProfileId': userProfile.id,
                                        'notification':notification,
                                        'ToolID':ToolID,
                                        'toolsRegister_temp':toolsRegister_temp,
                                        'form':form,
                                        'cannot_borrow':cannot_borrow,
                                        'requestedToDate':requestedToDate
                                        }))
                            


                    #apart from previous method, also save in new table
                    toolRequest = ToolRequest(toolId=ToolsRegister.objects.get(id=ToolID),
                                              requester_id=userProfile.user.username,
                                              requestedFromDate=form.cleaned_data['fromDate'],
                                              requestedToDate=form.cleaned_data['toDate'],
                                              requestStatus=0, #0 for pending
                                            )
                    toolRequest.save()
                    tool_req_succ_msg=True
                    print(tool_req_succ_msg)
                    context['tool_req_succ_msg']=tool_req_succ_msg
                    return HttpResponseRedirect('/borrowTools/')

                else:
                    form = ToFromDateForm()
                    ToolID = request.POST['IDForTheTool']
                    toolsRegister_temp = ToolsRegister.objects.get(id=ToolID)
                    context['form'] = form
                    context['invalid_form']=True
                    context['toolsRegister_temp']=toolsRegister_temp
                    return render_to_response('ToolManagement/borrowTool.html',
                        context_instance = RequestContext(request, context))
        else:
            form = ToFromDateForm()
            context['form'] = form
            #return render_to_response('ToolManagement/successToolRegistration.html')
    except ObjectDoesNotExist:

        context = {'message': 'There are no tools to borrow.','notification': notification}
        #return render_to_response('ToolManagement/borrowTools.html',
                               #    context)
    return render_to_response('ToolManagement/borrowTools.html',context_instance = RequestContext(request, context))

#this is Approve Tools in the frontend
@login_required
def viewRequests(request):
    userProfile = UserProfile.objects.get(user=request.user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    userProfileId = userProfile.id
    toolsRegister = ToolsRegister.objects.all()
    toolRequest = ToolRequest.objects.all()
    # to display no request message if not requested
    flag = False
    for object in toolsRegister:
        for object1 in toolRequest:
            if (object1.requestStatus == 0 and object1.requester_id != request.user.username and object.id == object1.toolId_id):
                flag = True
    context = {'userProfileId': userProfileId, 'toolsRegister': toolsRegister,'user':request.user, 'toolRequest':toolRequest, 'flag':flag,'notification': notification,'admin_notification':admin_notification}

    if request.method == 'POST' and 'rejectRequest' in request.POST:
        if request.POST.get('RequestID', False):
            form = RejectionReasonForm(request.POST)
            if form.is_valid():
                tool_RequestID = request.POST['RequestID']
                toolRequest = ToolRequest.objects.get(id=tool_RequestID)
                toolrejected = ToolRejected(toolId=toolRequest.toolId,
                                            requestId=toolRequest,
                                            requesterId=toolRequest.requester_id,
                                            rejectionReason=form.cleaned_data['rejectionReason'],
                                            notified = False,
                                          )
                toolrejected.save()
                toolRequest.requestStatus = 2 #rejected flag
                toolRequest.save()
                return HttpResponseRedirect('/myTools/requestedTool/')
    elif request.method == 'POST' and 'acceptRequest' in request.POST:
        if request.POST.get('RequestID', False):
            tool_RequestID = request.POST['RequestID']
            toolRequest = ToolRequest.objects.get(id=tool_RequestID)
            toolborrowed = ToolBorrowed(toolId=toolRequest.toolId,
                                        requestId=toolRequest,
                                        borrowerId=toolRequest.requester_id,
                                        notified=False,
                                      )
            toolborrowed.save()
            toolRequest.requestStatus = 1 #accepted/borrowed flag
            toolRequest.save()
            return HttpResponseRedirect('/myTools/requestedTool/')
    else:
        form = RejectionReasonForm()
        context['notification']= notification
        context['form'] = form
    return render_to_response('ToolManagement/viewRequests.html', context_instance = RequestContext(request, context))


@login_required
def returnTools(request):
    userProfile = UserProfile.objects.get(user=request.user)
    notification = checkRequest(userProfile)
    admin_notification = adminNotification(userProfile)
    toolsRegister = ToolsRegister.objects.all()
    toolRequest = ToolRequest.objects.all()
    context = {'toolsRegister':toolsRegister,
        'admin_notification':admin_notification,'notification':notification}
    flag = False
    for object in toolRequest:
        if object.requester_id == request.user.username and object.requestStatus == 1:
            flag = True
            context['toolRequest'] = toolRequest
            print('here at line 467')
            #I don't know how to find the difference between requestToDate and today's date so that it would be nice to
            #display time remaining for the tool to be returned to the user
    context['flag'] = flag
    if request.method == 'POST':
        form = ToolReturnForm(request.POST)
        if form.is_valid():
            print('jkjskjfsd')
            if request.POST.get('IDForTheTool', True):
                tool_RequestID = request.POST['RequestID']
                toolRequest = ToolRequest.objects.get(id=tool_RequestID)
                toolReturned = ToolReturn(toolId=toolRequest.toolId,
                                            requestId=toolRequest,
                                            note=form.cleaned_data['note'],
                                            rating=form.cleaned_data['rating'],
                                            )
                toolReturned.save()
                toolRequest.requestStatus = 4  # returned flag
                toolRequest.save()
                print("returned")
                return HttpResponseRedirect('/myTools/returnTools/')
        else:
            print('sfdsfsfsdf')
            form = ToolReturnForm()
            context['form'] = form
            context['invalid_form'] = True
            return render_to_response('ToolManagement/returnTools.html', 
                context_instance = RequestContext(request, context))

    else:
        form = ToolReturnForm()
        context['form'] = form
    return render_to_response('ToolManagement/returnTools.html', context_instance = RequestContext(request, context))

@login_required
def myRequests(request):
    userProfile = UserProfile.objects.get(user=request.user)
    notification = checkRequest(userProfile)
    admin_notification = adminNotification(userProfile)
    userProfileId = userProfile.id
    toolRejected = ToolRejected.objects.all().filter(requesterId=userProfile.user.username)
    toolBorrowed = ToolBorrowed.objects.all().filter(borrowerId=userProfile.user.username)
    toolRequest = ToolRequest.objects.all().filter(requester_id=userProfile.user.username)
    toolsRegister = ToolsRegister.objects.all()
    context = {'user':request.user,'userProfileId': userProfileId, 'toolsRegister': toolsRegister,
     'toolRejected': toolRejected, 'toolBorrowed': toolBorrowed, 'toolRequest' : toolRequest,
     'notification':notification,
        'admin_notification':admin_notification}
    return render_to_response('ToolManagement/myRequests.html', context)

@login_required
def otherAcceptedRequests(request):
    userProfile = UserProfile.objects.get(user=request.user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    userProfileId = userProfile.id
    toolsRegister = ToolsRegister.objects.all()
    context = {'userProfileId' : userProfileId, 'toolsRegister':toolsRegister,'notification':notification,
        'admin_notification':admin_notification}
    return render_to_response('ToolManagement/listOfAcceptedRequest.html', context)

@login_required
def ShareZoneView(request):
    user=request.user
    userProfile = UserProfile.objects.get(user=user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    users = UserProfile.objects.filter(zipCode = userProfile.zipCode)
    zipcode = ShareZone.objects.get(zipCode=userProfile.zipCode)
    template = loader.get_template('ShareZone.html')
    context = {
        'ShareZone': zipcode,
        'userProfile': userProfile,
        'users': users,
        'notification':notification,
        'admin_notification':admin_notification
    }
    return HttpResponse(template.render(context, request))


def is_member(user):
    return user.groups.filter(name='admin_user').exists()

@login_required
@user_passes_test(is_member)
def CreateCommunityShed(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    Sharezone = ShareZone.objects.get(zipCode = userProfile.zipCode)
    if request.method == 'POST' and 'CreateShed' in request.POST:
        form = CommunityShedCreation(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']


            Sharezone.CommunityShedLocation = address
            Sharezone.has_CommunityShed = True
            Sharezone.save()

            return HttpResponseRedirect('/ShareZone/')
    elif request.method == 'POST' and 'Cancel' in request.POST:

            return HttpResponseRedirect('/ShareZone/')
    else:
        form = CommunityShedCreation()
        variables = RequestContext(request, {
            'form': form,'notification':notification})

    return render_to_response('cshed.html', context_instance=RequestContext(request,
                            {'form': form,'notification':notification,
        'admin_notification':admin_notification}))

@login_required
@user_passes_test(is_member)
def ShareZoneUsersView(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    users = UserProfile.objects.all().filter(ShareZone=userProfile.ShareZone)
    users1 = users.filter(request=False)


    context = {
        'ShzU': users,
        'user': user,
        'users1': users1,
        'notification':notification,
        'admin_notification':admin_notification
    }


    if request.method == 'POST' and 'acceptRequest' in request.POST:

        username = request.POST.get('RequestID')
        user1 = UserProfile.objects.get(pk = username)
        user1.user.is_active = True
        user1.request = True
        user1.save()
        user1.user.save()

        return HttpResponseRedirect('/ShareZoneUsers/')

    elif request.method == 'POST' and 'rejectRequest' in request.POST:
        username = request.POST.get('RequestID')
        user1 = UserProfile.objects.get(pk = username)
        user1.user.delete()
        user1.delete()

        return HttpResponseRedirect('/ShareZoneUsers/')

    return render_to_response('ShareZoneUsers.html', context_instance=RequestContext(request, context))

@user_passes_test(is_member)
@login_required
def ManageUsers(request):
    user1 = request.user
    userProfile = UserProfile.objects.get(user=user1)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    Sharezone = UserProfile.objects.filter(ShareZone=userProfile.ShareZone, request=True)
    g = Group.objects.get(name='admin_user')

    context = {
        'ShZ': Sharezone,
        'notification': notification,
        'admin_notification':admin_notification
    }
    if request.method == 'POST' and 'Deactivate' in request.POST:
        username = request.POST.get('RequestID')
        user2 = UserProfile.objects.get(user=username)
        user2.user.is_active=False
        user2.user.save()
        user2.save()


        return HttpResponseRedirect('/ManageUsers/')

    elif request.method == 'POST' and 'Activate' in request.POST:
        username = request.POST.get('RequestID')
        user2 = UserProfile.objects.get(user=username)
        user2.user.is_active = True
        user2.user.save()
        user2.save()

        return HttpResponseRedirect('/ManageUsers/')

    elif request.method == 'POST' and 'makeAdmin' in request.POST:
        username = request.POST.get('RequestID')
        g = Group.objects.get(name='admin_user')
        user3 = UserProfile.objects.get(user = username)
        user3.is_admin = True

        user3.save()
        g.user_set.add(username)

    return render_to_response('ManageUsers.html',context_instance = RequestContext(request, context))

@user_passes_test(is_member)
@login_required
def UpdateUser(request, user_id):
    shzadmin = request.user
    shzadmin1 = UserProfile.objects.get(user = shzadmin)
    user = User.objects.get(pk= user_id)
    userProfile = UserProfile.objects.get(user = user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    user1 = request.user
    userProfile1 = UserProfile.objects.get(user = user1)
    notification = checkRequest(userProfile1)

    if shzadmin1.ShareZone != userProfile.ShareZone:
        return HttpResponseRedirect('../../UsersPermission/')

    else:
        if 'cancel' in request.POST:
            return HttpResponseRedirect('/home/')

        elif request.method == 'POST' and 'Save' in request.POST:
            form = UserProfileForm(request.POST)
            if form.is_valid():
                user.email = form.cleaned_data['email']
                userProfile.first_Name = form.cleaned_data['first_Name']
                userProfile.last_Name = form.cleaned_data['last_Name']
                userProfile.zipCode = form.cleaned_data['zipCode']
                userProfile.address = form.cleaned_data['address']
                userProfile.pickupArrangements = form.cleaned_data['pickupArrangements']
                userProfile.date = form.cleaned_data['date1']
                user.save()
                userProfile.save()
                variables = RequestContext(request, {
                    'form': form
                })
                return HttpResponseRedirect('/ManageUsers/')
        else:
            form = UserProfileForm()
            form.fields['username'].initial = user.username
            form.fields['email'].initial = user.email
            form.fields['first_Name'].initial = userProfile.first_Name
            form.fields['last_Name'].initial = userProfile.last_Name
            form.fields['zipCode'].initial = userProfile.zipCode
            form.fields['address'].initial = userProfile.address
            form.fields['pickupArrangements'].initial = userProfile.pickupArrangements
            form.fields['date1'].initial = userProfile.date

        return render_to_response('UpdateUser.html',
         context_instance=RequestContext(request,
            {'form': form,'notification': notification,
        'admin_notification':admin_notification}))

@login_required
@user_passes_test(is_member)
def noPermission(request):
    return render_to_response('UsersPermission.html')

@login_required
@user_passes_test(is_member)
def noPermission_tool(request):
    return render_to_response('ToolsPermission.html')
@login_required
@user_passes_test(is_member)
def ManageTools(request):
    user1 = request.user
    userProfile = UserProfile.objects.get(user=user1)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    Sharezone = UserProfile.objects.filter(ShareZone=userProfile.ShareZone)
    tools = ToolsRegister.objects.filter(userProfile = Sharezone)

    context = {
        'tools': tools,
        'notification':notification,
        'admin_notification':admin_notification
    }

    if request.method == 'POST' and 'changeActivation' in request.POST:
        if request.POST.get('IDForTheTool', False):
            ToolID = request.POST['IDForTheTool']
            toolsRegister_temp = ToolsRegister.objects.get(id=ToolID)
            if toolsRegister_temp.statusOfTheTool == 'Available':
                toolsRegister_temp.statusOfTheTool = 'Unavailable'
                toolsRegister_temp.save()
            else:
                toolsRegister_temp.statusOfTheTool = 'Available'
                toolsRegister_temp.save()
                return HttpResponseRedirect('/ManageTools/')


    return render_to_response('ManageTools.html',context_instance = RequestContext(request, context))

@user_passes_test(is_member)
@login_required
def UpdateTool(request, tool_id):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    admin_notification = adminNotification(userProfile)
    notification = checkRequest(userProfile)
    Sharezone = ShareZone.objects.get(zipCode=userProfile.zipCode)
    tool = ToolsRegister.objects.get(pk = tool_id)

    if userProfile.ShareZone != tool.userProfile.ShareZone:
        return HttpResponseRedirect('../../ToolsPermission/')

    else:

        if request.method == 'POST' and 'Update' in request.POST:
            form = ToolUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                toolAvailChoice = form.cleaned_data['addressOfTheTool']
                if toolAvailChoice == 'Home':
                    addressOfTheTool = tool.userProfile.address
                else:
                    if Sharezone.has_CommunityShed == True:
                        addressOfTheTool = 'Community Shed'
                    else:
                        addressOfTheTool = tool.userProfile.address

                tool.addressOfTheTool = form.cleaned_data['addressOfTheTool']
                tool.statusOfTheTool = form.cleaned_data['statusOfTheTool']
                tool.categoryOfTheTool = form.cleaned_data['categoryOfTheTool']
                print(form.cleaned_data['image'])
                if form.cleaned_data['image'] != None:
                    tool.image = form.cleaned_data['image']
                tool.conditionOfTheTool = form.cleaned_data['conditionOfTheTool']
                tool.toolDescription = form.cleaned_data['toolDescription']
                tool.save()
                return HttpResponseRedirect('/ManageTools/')
                #return render_to_response('ManageTools.html', context_instance=RequestContext(request,
                                                                #{
                                                                 #                                                      'alert': True,
                                                                  #                                                     'succ_msg': 'Tool Information Updated Successfully.'}))
        else:
            form = ToolUpdateForm()
            form.fields['nameOfTheTool'].initial = tool.nameOfTheTool
            form.fields['addressOfTheTool'].initial = tool.addressOfTheTool
            form.fields['categoryOfTheTool'].initial = tool.categoryOfTheTool
            form.fields['conditionOfTheTool'].initial = tool.conditionOfTheTool
            form.fields['toolDescription'].initial = tool.toolDescription
            #form.fields['image'].initial=tool.image

        return render_to_response('UpdateTool.html',
         context_instance=RequestContext(request, 
            {'form': form,
            'tool_image_url': tool.image.url,
            'admin_notification':admin_notification,
            'notification':notification}))

def is_member2(user):
    return user.groups.filter(name='system_admin').exists()
#the code below is for system_admin

@user_passes_test(is_member2)
@login_required
def ManageUsersAdmin (request):
    user1 = request.user
    userProfile = UserProfile.objects.get(user=user1)
    Sharezone = UserProfile.objects.all()

    context = {
        'ShZ': Sharezone,

        }
    if request.method == 'POST' and 'Deactivate' in request.POST:
        username = request.POST.get('RequestID')
        user2 = UserProfile.objects.get(user=username)
        user2.user.is_active = False
        user2.user.save()
        user2.save()

        return HttpResponseRedirect('/ManageUsersAdmin/')

    elif request.method == 'POST' and 'Activate' in request.POST:
        username = request.POST.get('RequestID')
        user2 = UserProfile.objects.get(user=username)
        user2.user.is_active = True
        user2.user.save()
        user2.save()

        return HttpResponseRedirect('/ManageUsersAdmin/')

    elif request.method == 'POST' and 'makeAdmin' in request.POST:
        username = request.POST.get('RequestID')
        user = User.objects.get(pk = username)
        g = Group.objects.get(name='admin_user')
        h = Group.objects.get(name='basic_user')
        user3 = UserProfile.objects.get(user=username)
        user3.is_admin = True

        user3.save()

        user.groups.remove(h)
        g.user_set.add(user)

    elif request.method == 'POST' and 'makeUser' in request.POST:
        username = request.POST.get('RequestID')
        user = User.objects.get(pk=username)
        userpro = UserProfile.objects.get(user=user)
        admins = UserProfile.objects.filter(zipCode =userpro.zipCode, is_admin=True)
        if len(admins) == 1:
            return HttpResponseRedirect('/CannotRemoveUser/')
        else:
            c = Group.objects.get(name='basic_user')
            d = Group.objects.get(name='admin_user')
            user4 = UserProfile.objects.get(user=username)
            user4.is_admin = False

            user4.save()

            user.groups.remove(d)
            c.user_set.add(username)



    return render_to_response('ManageUsersAdmin.html', context_instance=RequestContext(request, context))

def CannotRemoveUser(request):
    return render_to_response('CannotRemoveUser.html')

@user_passes_test(is_member2)
@login_required
def UpdateUserAdmin (request, user_id):
    shzadmin = request.user
    user = User.objects.get(pk=user_id)
    userProfile = UserProfile.objects.get(user=user)

    form1=UserProfileForm()
    if 'cancel' in request.POST:
        return HttpResponseRedirect('/home/')

    elif request.method == 'POST' and 'Save' in request.POST:
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            userProfile.first_Name = form.cleaned_data['first_Name']
            userProfile.last_Name = form.cleaned_data['last_Name']
            userProfile.zipCode = form.cleaned_data['zipCode']
            userProfile.address = form.cleaned_data['address']
            userProfile.pickupArrangements = form.cleaned_data['pickupArrangements']
            userProfile.date = form.cleaned_data['date1']
            user.save()
            userProfile.save()
            variables = RequestContext(request, {
                            'form': form,
            'admin_notification':admin_notification,'notification':notification
                        })
            return HttpResponseRedirect('/ManageUsersAdmin/')

    else:
        form = UserProfileForm()
        form.fields['username'].initial = user.username
        form.fields['email'].initial = user.email
        form.fields['first_Name'].initial = userProfile.first_Name
        form.fields['last_Name'].initial = userProfile.last_Name
        form.fields['zipCode'].initial = userProfile.zipCode
        form.fields['address'].initial = userProfile.address
        form.fields['pickupArrangements'].initial = userProfile.pickupArrangements
        form.fields['date1'].initial = userProfile.date

    return render_to_response('UpdateUser.html', context_instance=RequestContext(request, {'form': form,}))



@login_required
@user_passes_test(is_member2)
def ManageToolsAdmin (request):
    user1 = request.user
    userProfile = UserProfile.objects.get(user=user1)
    tools = ToolsRegister.objects.all()

    context = {
        'tools': tools,

    }

    if request.method == 'POST' and 'changeActivation' in request.POST:
        if request.POST.get('IDForTheTool', False):
            ToolID = request.POST['IDForTheTool']
            toolsRegister_temp = ToolsRegister.objects.get(id=ToolID)
            if toolsRegister_temp.statusOfTheTool == 'Available':
                toolsRegister_temp.statusOfTheTool = 'Unavailable'
                toolsRegister_temp.save()
            else:
                toolsRegister_temp.statusOfTheTool = 'Available'
                toolsRegister_temp.save()
                return HttpResponseRedirect('/ManageToolsAdmin/')

    return render_to_response('ManageToolsAdmin.html', context_instance=RequestContext(request, context))

@login_required
@user_passes_test(is_member2)
def ManageSharezone (request):
    user1 = request.user
    userProfile = UserProfile.objects.filter(is_admin = True)
    Sharezone = ShareZone.objects.all()


    context = {
        'Shz': Sharezone,
        'users': userProfile,

    }

    return render_to_response('ManageSharezone.html', context_instance=RequestContext(request, context))

@login_required
@user_passes_test(is_member2)
def UpdateShed(request, shz_id):

    shzone = ShareZone.objects.get(pk = shz_id)

    if request.method == 'POST' and 'CreateShed' in request.POST:
        form = CommunityShedCreation(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            shzone.CommunityShedLocation = address
            shzone.has_CommunityShed = True;

            shzone.save()

            return HttpResponseRedirect('/ManageSharezone/')

    elif request.method == 'POST' and 'Cancel' in request.POST:

        return HttpResponseRedirect('/ManageSharezone/')

    else:
        form = CommunityShedCreation()
        variables = RequestContext(request, {
             'form': form})

    return render_to_response('UpdateShed.html', 
        context_instance=RequestContext(request,
            {'form': form}))


@user_passes_test(is_member2)
@login_required
def UpdateToolAdmin(request, tool_id):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    tool = ToolsRegister.objects.get(pk = tool_id)
    Sharezone = ShareZone.objects.get(zipCode=tool.userProfile.zipCode)


    if request.method == 'POST' and 'Update' in request.POST:
        form = ToolUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            toolAvailChoice = form.cleaned_data['addressOfTheTool']
            if toolAvailChoice == 'Home':
                addressOfTheTool = tool.userProfile.address
            else:
                if Sharezone.has_CommunityShed == True:
                    addressOfTheTool = 'Community Shed'
                else:
                    addressOfTheTool = tool.userProfile.address

                    tool.addressOfTheTool = form.cleaned_data['addressOfTheTool']
                    tool.statusOfTheTool = form.cleaned_data['statusOfTheTool']
                    tool.categoryOfTheTool = form.cleaned_data['categoryOfTheTool']
                    print(form.cleaned_data['image'])
                    if form.cleaned_data['image'] != None:
                        tool.image = form.cleaned_data['image']
                    tool.conditionOfTheTool = form.cleaned_data['conditionOfTheTool']
                    tool.toolDescription = form.cleaned_data['toolDescription']
                    tool.save()

                    return HttpResponseRedirect('/ManageToolsAdmin/')


                        # return render_to_response('ManageTools.html', context_instance=RequestContext(request,
                        # {
                        #                                                      'alert': True,
                        #                                                     'succ_msg': 'Tool Information Updated Successfully.'}))
    else:
        form = ToolUpdateForm()
        form.fields['nameOfTheTool'].initial = tool.nameOfTheTool
        form.fields['addressOfTheTool'].initial = tool.addressOfTheTool
        form.fields['categoryOfTheTool'].initial = tool.categoryOfTheTool
        form.fields['conditionOfTheTool'].initial = tool.conditionOfTheTool
        form.fields['toolDescription'].initial = tool.toolDescription
        form.fields['image'].initial = tool.image

    return render_to_response('UpdateTool.html', 
        context_instance=RequestContext(request, {'form': form,
            'tool_image_url': tool.image.url}))
