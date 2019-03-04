module ochozi {

  struct Zone {
    string identifier;
    short value;
  };

  sequence<Zone> ZoneSeq;
  sequence<bool> OutputValueSeq;

  struct NodeStatus {
    ZoneSeq zones;
    OutputValueSeq outputs;
  };

  interface Listener {
    void report(NodeStatus node);
  };

  interface Node {
    void setOutputs(OutputValueSeq outputs);
  };
};
