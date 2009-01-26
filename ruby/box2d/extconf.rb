#!/usr/bin/env ruby

#Run this file, then 'make' and 'sudo make install' to build ruby bindings for Box2D
require 'mkmf'
require 'erb'

raise 'You must specify the location of the Box2D directory' unless ARGV[0]

BOX2D_DIR = ARGV[0]


CONFIG['CC'] = 'g++'

includes = Dir["#{BOX2D_DIR}/Source/**/b2*.h"]

swig_file = <<END
%include exception.i  

%include <ruby.swg>

%feature("compactdefaultargs");

%typemap(in) void* {
	$1 = (void*)($input);
}

%typemap(out) void* {
    $result = (VALUE)($1);
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER) void * {
	$1 = TRUE;
} 

// special handling of box2d lists
%typemap(in) b2Shape ** {
 int size = RARRAY($input)->len; 
 $1 = (b2Shape **) calloc(size+1,sizeof(b2Shape*));
}

%typemap(argout) b2Shape ** {
	b2Shape** lst = $1;
	b2Shape** it = $1;
	int n = 0;
	while(*it != 0) {
		++it;
		++n;
	}

	for ( int i = 0; i < n;  i++ ) {
		rb_ary_store($input, i, SWIG_NewPointerObj(lst[i],SWIGTYPE_p_b2Shape,0)); 
	}
	free((b2Shape *) $1);
}

// supports adding b2Vec2
%extend b2Vec2 {
	b2Vec2 operator+(const b2Vec2& other)
	{
		return b2Vec2(self->x + other.x, self->y + other.y);
	}
}

// typecast hack

%extend b2Joint {
 b2MouseJoint* get_as_mouse_joint(){
	return static_cast<b2MouseJoint*>(self);
 }
}
%module box2d
%{
#{includes.map { |i| "#include \"#{i}\"" }.join "\n"}
%}

#{includes.map { |i| "%include \"#{i}\"" }.join "\n"}
END

open('box2d.i', 'w') { |f| f << swig_file }
raise 'box2d libary not found' unless have_library('box2d')
system 'swig -c++ -ruby box2d.i' or raise 'could not build wrapper via swig'
create_makefile('box2d')
