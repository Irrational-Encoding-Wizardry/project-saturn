# Executing code
Executing the code is one of the core features an Editor for VapourSynth must provide. Also the user might want to preview the outputs of the script.

## Operations
### run
Creating a new core is important as otherwise pre-existing variables may interfere with the script that the user wants to execute.
How the core is created and where its VapourSynth-Core will actually live is defined by the concrete implementation of the `AbstractCore`
class.

```
User      EditorContext(1)     AbstractCore(2)
 |              |                    |
 |====run()====>|                    |
 |              | ====restart()====> |
 |              |                    |====\
 |              |                    |    | stop()
 |              |                    ||<==/
 |              |                    ||---\
 |              |                    |    |
 |              |                    |<---/
 |              |                    |====\
 |              |                    |    | start()
 |              |                    ||<==/
 |              |                    ||---\
 |              |                    |    |
 |              |                    |<---/
 |              | <----------------- |
 |              | ==push_script()==> |
 |              | <----------------- |
 |<------------ |                    |
 ```

### preview
The preview-function will first try to receive an `AbstractClip`-instance that acts as a remote Proxy[GOF207] to the actual `VideoNode`-instance.
It will then try to retrieve a frame from the clip whenever a frame is needed.

```
User      EditorContext(1)     AbstractCore(2)
 |==preview()==>|                    |
 |              | ==get_output()===> |                    
 |              |                    | ======CREATE======> AbstractClip
 |              |                    | <----------------------- |
 |              | <----------------- |                          |
 |<------------ |                    |                          |
 |===========================get_frame()=======================>|
 |<-------------------------------------------------------------|
```

## References
GOF207: “Proxy.” Design Patterns: Elements of Reusable Object-Oriented Software, by Erich Gamma, Addison-Wesley, 1995, pp. 207–217.
