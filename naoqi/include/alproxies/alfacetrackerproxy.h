// Generated for ALFaceTracker version 1.14

#ifndef ALFACETRACKERPROXY_H_
#define ALFACETRACKERPROXY_H_
#include <alproxies/alfacetrackerproxyposthandler.h>

#include <alproxies/api.h>



namespace AL
{
class ALBroker;
class ALProxy;

class ALFaceTrackerProxyImpl;

/// <summary>This module is dedicated to track a face. When activated, Nao will move its head to follow the detected face.
    ///
    ///  This module relies on ALFaceDetection, so be sure it is loaded on your robot.</summary>
/// \ingroup ALProxies
class ALPROXIES_API ALFaceTrackerProxy
{
  private:
    boost::shared_ptr<ALFaceTrackerProxyImpl> fImpl;
    void xInit();

  public:
    /// <summary>
    /// Default Constructor. If there is a broker in your process, which is always the case
    /// if you are in a module, then this will be found and used.
    /// </summary>
    ALFaceTrackerProxy();

    /// <summary>
    /// Explicit Broker Constructor. If you have a smart pointer to a broker that you want
    /// to specify, then you can use this constructor. In most cases, the default constructor
    /// will do the work for you without passing a broker explicitly.
    /// </summary>
    /// <param name="broker">A smart pointer to your broker</param>
    ALFaceTrackerProxy(boost::shared_ptr<ALBroker> broker);

    /// <summary>
    /// Explicit Proxy Constructor. Create a specialised proxy from a generic proxy.
    /// </summary>
    /// <param name="broker">A smart pointer to your broker</param>
    ALFaceTrackerProxy(boost::shared_ptr<ALProxy> proxy);


    /// <summary>
    /// Remote Constructor. This constructor allows you to connect to a remote module by
    /// explicit IP address and port. This is useful if you are not within a process that
    /// has a broker, or want to connect to a remote instance of NAOqi such as another
    /// robot.
    /// </summary>
    /// <param name="ip">The IP address of the remote module you want to connect to</param>
    /// <param name="port">The port of the remote module, typically 9559</param>
    ALFaceTrackerProxy(std::string ip, int port=9559);

    /// <summary>
    /// Implements thread wrappers around methods
    /// </summary>
    ALFaceTrackerProxyPostHandler post;

    // --- access to ALProxy ----

    /// <summary>
    /// Gets the underlying generic proxy
    /// </summary>
    boost::shared_ptr<ALProxy> getGenericProxy();

    // ------------------------------

    /// <summary>
    /// Exits and unregisters the module.
    /// </summary>
    void exit();

    /// <summary>
    /// Gets the name of the parent broker.
    /// </summary>
    /// <returns> The name of the parent broker. </returns>
    std::string getBrokerName();

    /// <summary>
    /// Retrieves a method's description.
    /// </summary>
    /// <param name="methodName"> The name of the method. </param>
    /// <returns> A structure containing the method's description. </returns>
    AL::ALValue getMethodHelp(const std::string& methodName);

    /// <summary>
    /// Retrieves the module's method list.
    /// </summary>
    /// <returns> An array of method names. </returns>
    std::vector<std::string> getMethodList();

    /// <summary>
    /// Retrieves the module's description.
    /// </summary>
    /// <returns> A structure describing the module. </returns>
    AL::ALValue getModuleHelp();

    /// <summary>
    /// Return the [x, y, z] position of the face in FRAME_TORSO. This is done assuming an average face size, so it might not be very accurate.
    ///
    ///  This invalidates the isNewData field of the tracker. See isNewData()) for more details.
    /// </summary>
    /// <returns> An Array containing the face position [x, y, z]. </returns>
    std::vector<float> getPosition();

    /// <summary>
    /// Gets the method usage string. This summarises how to use the method.
    /// </summary>
    /// <param name="name"> The name of the method. </param>
    /// <returns> A string that summarises the usage of the method. </returns>
    std::string getUsage(const std::string& name);

    /// <summary>
    /// Return true if the face Tracker is running.
    /// </summary>
    /// <returns> true if the face Tracker is running. </returns>
    bool isActive();

    /// <summary>
    /// Return true if a new face was detected since the last getPosition().
    /// </summary>
    /// <returns> true if a new face was detected since the last getPosition(). </returns>
    bool isNewData();

    /// <summary>
    /// Returns true if the method is currently running.
    /// </summary>
    /// <param name="id"> The ID of the method that was returned when calling the method using 'post' </param>
    /// <returns> True if the method is currently running </returns>
    bool isRunning(const int& id);

    /// <summary>
    /// Just a ping. Always returns true
    /// </summary>
    /// <returns> returns true </returns>
    bool ping();

    /// <summary>
    /// if true, the tracking will be through a Whole Body Process.
    /// </summary>
    /// <param name="pWholeBodyOn"> The whole Body state </param>
    void setWholeBodyOn(const bool& pWholeBodyOn);

    /// <summary>
    /// Start the tracker by Subscribing to Event FaceDetected from ALFaceDetection module.
    ///
    /// Then Wait Event FaceDetected from ALFaceDetection module.
    ///
    /// And finally send information to motion for head tracking.
    ///
    /// NOTE: Stiffness of Head must be set to 1.0 to move!
    /// </summary>
    void startTracker();

    /// <summary>
    /// returns true if the method is currently running
    /// </summary>
    /// <param name="id"> the ID of the method to wait for </param>
    void stop(const int& id);

    /// <summary>
    /// Stop the tracker by Unsubscribing to Event FaceDetected from ALFaceDetection module.
    /// </summary>
    void stopTracker();

    /// <summary>
    /// Returns the version of the module.
    /// </summary>
    /// <returns> A string containing the version of the module. </returns>
    std::string version();

    /// <summary>
    /// Wait for the end of a long running method that was called using 'post'
    /// </summary>
    /// <param name="id"> The ID of the method that was returned when calling the method using 'post' </param>
    /// <param name="timeoutPeriod"> The timeout period in ms. To wait indefinately, use a timeoutPeriod of zero. </param>
    /// <returns> True if the timeout period terminated. False if the method returned. </returns>
    bool wait(const int& id, const int& timeoutPeriod);

};

}
#endif // ALFACETRACKERPROXY_H_

