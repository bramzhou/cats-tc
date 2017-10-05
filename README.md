# C-ATS Node 5.1.0 Release Notes #

[![N|Solid](http://www.cienet.com/wp-content/uploads/2017/01/logo_80_1x.png)](http://www.cienet.com/cienet-automated-test-solution-for-in-vehicle-infotainment-system)

This document describes new features and backward compatilities for C-ATS Nodes 5.1.0.

## Backward Compatilities ##
The release 5.1.0 keeps compatible with previous release with following exceptions.

 - New XML attribute retryEnabled in testcase-def is added to enable ADB retry. By default
   retryEnabled is true. In case ADB retry failed, the case will be aborted. Test case has
   to disable ADB retry by setting retryEnabled to false.
   ```XML
   <testcase-def logicName="example" retryEnabled="false">
   ```
 - Strings including ${xxx} need to be escaped by \'\\\'. In 5.1.0, the variable vaule can be refered by ${variable}. So any string including ${xxx} will be interpreted as a variable. To keep the ${xxx} as part of string, \'\\\' has to be put in front of $.
    ```XML
    <var name="v1">C-ATS</var>
    <var name="example">this is ${v1}</var>  --> example=this is C-ATS
    <var name="example">this is \${v1}</var> --> example=this is ${v1}
    ```  
 - Space escape in AgentHelper should be removed.
 - takeSnapshot attribute won't be supported. Only snapshot attribute will be supported.
   ```XML
   <action name="Comments" >
     <param name="comments">This is comments</param>
     <param name="takeSnapshot">true</param>
   </action>
   ```
   should be changed to:
   ```XML
   <action name="Comments" >
     <param name="comments">This is comments</param>
     <param name="snapshot">true</param>
   </action>
   ```



## New Features ##

  - XML Syntax Enhancements

  - Python Support

  - Logging Enhancements

  - Dryrun Support

  - Action Meta Support (for Action developers)

### I. XML Syntax Enhancements ###
1. New subcase definition  
Subcase is recommended to replace operation. To keep the backward compatilities, both subcase and operation are supported on Node 5.1.0.
  a. Very similar like function call  
  b. All subcases should be put in subcase directory  
  c. Calling parameter name should be the same as specified in subcase-interface-input  
  d. subcase-interface-output is information only, put return value specification in it if has  
Examples:
    ```XML
    <subcase path="example" result="output">
      <param name="deviceID">${MUTDevice}</param>
    </subcase>

    <subcase-def logicName="example">
      <interface>
        <input name="deviceID" />
        <output info="output is a boolean" type="bool"/>
      </interface>
      <var name="result">true</var>
      <return>${result}</return>
    </subcase-def>

    ```
2. Variable setter and getter  
a. Variable scope is in the same file, undefined variable will be assumed "global" which should be defined in properties  
b. String include \$\{\.\.\} should be escaped by "\\", i.e. \\\$\{\.\.\}  
c. Data type support "string", "bool", "int", "float" and "map"  
Examples:
      ```XML
      <var name="var1" type="int">123</var>
      	<var name="var2" />
      	<var name="map_var1">
      		<map>
      			<entry key="key1" type="string">this is string</entry>
      			<entry key="key2">${var1}</entry>
      		</map>
      </var>
      <setvar name="var2">${var1}</setvar>
      <var name="var3" type="int">${map_var1.key2}</var>

      ```
      variable can also be used in action and loop attributes:
      ```XML
      <action name="Press" sleep="${sleepTime}">
      <loop gaugeValue="${maxLoopTimes}" increment="1" initValue="${loopInitValue}">
      ```

3. if-else support  
  if-else intend to replace \<block if="exp">.  
  Examples:
      ```XML
      <if exp="condition" >
           <some actions 1>
        <else>
           <some actions 2>
        </else>
      </if>
      ```
      if condition is true, "some action 1" will be executed. Otherwise "some actions 2" will be executed.
      Conditions can be complex expressions like following:
      ```XML
      <if exp="${var2} eq (120 + 3)">
            <log >condition is met</log>
            <else>
                <log >condition is not met</log>
            </else>
      </if>

      <if exp="((${var5} - 125) lt 0) and (${var3} eq false) and (${var2} gt 122)">
            <log >condition is met</log>
            <else>
                <log >condition is not met</log>
            </else>
      </if>

      ```
      >Supported logic expression: and, or  
      >Supported comparison expression: eq, lt(<),gt(>)  
      >Supported math expression: +, -, \*, \/, \%  
      >Supported string expression: in(included), ct(contain), mt(match)
      > if-else can be nested

### II. Python Support ###
1. Support Jython 2.7.1 which is mostly compatible with Python 2.7
2. Only dependency is JDK 7 and above
3. Jython is built into the Node, no need to install it separately
4. 3rd party python library need to be installed separately
5. 3rd party python libraries need call C library are not supported
6. Node executes python based test cases the same way as xml based test cases
    - Put python test cases into cases/ directory (\*.py)
    - Construct tasks.xml
    - Run tasks
7. In case of python multithread support, actions can NOT be used in thread yet

Python Related Configurations:
```
config/tms.properties:
  pylib.path=operation;subcase;/home/user/pylib
  or
  pylib.path=operation;subcase;C:\\Users\\mats\\pylib
```

### III. Logging Enhancements ###
1. Task log and case log are enhanced to output concise and meaningful logs
2. Add New Performance Log

### IV. Dryrun Support
1. Node can be set to Dryrun mode
2. In Dryrun mode, test will be run as usual except that actions won't be executed and all sleep will be skipped
3. Dryrun mode can be set through TMS WebUI
4. For debug-tool, adding following configuration can set Node in Dryrun mode
```
config/tms.properties:
  node.mode=test_mode
```

### V. Action Meta Support (for Action developers) ###

New Action development is based on Action-Meta:
  - Define action in action meta:
      ```XML
      <Action actionName="FakeWithReturnString"
         handler="com.cienet.blee.handler.SnapshotActionHandler"
         info="This fake action has return. return value equals to e
              xpected input parameter">    
        <InputParam name="expected" type="Map"
          info="set expected return value to control verification"/>    
        <InputParam name="isThrowException" type="Boolean" required="false"
           defaultValue="false" info="throw ActionException if set to true. Default value is false."/>   
        <OutputParam type="Map" info="A string variable defined to store the verification result"/>
      </Action>
      ```
  - Build project and generate the action base class and action class
  - Move action class to actions directory adn Implement doAction method in action class
    ```java
    public class FakeWithReturnStringAction extends FakeWithReturnStringBaseAction {
         private static final Logger log = Logger.getLogger(FakeWithReturnStringAction.class);    
         @Override
         public Map<String, Object> doAction(IActionContext context, Map<String, Object> expected, Boolean isThrowException) throws ActionException {        
           // TODO        
           return null;    
         }    
         @Override    
         public Map<String, Object> getDryRunResult() {
           // TODO        
           return null;    
         }
       }

    ```


#### @Copyright
CIeNET Technologies
