package com.yektaie.graph.io;

public interface Factory<Type> {
    Type newInstance(String str);
}
